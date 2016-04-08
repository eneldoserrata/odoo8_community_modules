import base64
import datetime
from openerp.osv import osv
from openerp.addons.web import http
from openerp.exceptions import except_orm, Warning
import openerp.addons.web.http as oeweb
from openerp import models, fields, api, _
import openerp
from operator import attrgetter
try:
    import xlwt
except ImportError:
    xlwt = None
import re
from cStringIO import StringIO



class ir_exports( models.Model ):
    _name = "ir.exports"
    _inherit = ['ir.exports', 'mail.thread', 'ir.needaction_mixin']

    @api.one
    @api.depends( 'resource' )
    def get_model_name( self ):
        if self.resource:
            model_obj = self.env['ir.model'].search( [( 'model', '=', self.resource )] )
            if model_obj :
                self.model_name = model_obj[0].name


    model_name = fields.Char( 'Model', compute=get_model_name , store=True )
    domain = fields.Char( string='Domain' )
    file_name = fields.Char( string='Filename', size=255 )
    color = fields.Integer( string='Color Index' )
    attachment_id = fields.Many2one( 'ir.attachment', string="Attachments" )
    attachment_date = fields.Datetime( related='attachment_id.create_date', string="Last Attachment Date" )
    export_fields = fields.One2many( order='sequence,heading,name' )
    notes = fields.Html( 'Notes' )

    @api.multi
    def popup_wizard( self ):
        if self._context is None:
            self._context = {}
        ir_model_data = self.env['ir.model.data']
        try:
            compose_form_id = ir_model_data.get_object_reference( 'ir_export_extended_ept', 'export_wizard_view_ept' )[1]
        except ValueError:
            compose_form_id = False
        return {
            'name': _( 'Export File' ),
            'res_model': 'export.wizard.ept',
            'type': 'ir.actions.act_window',
            'view_id': compose_form_id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

    def from_data( self, fields, rows ):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet( 'Sheet 1' )
        header_title = xlwt.easyxf( "font: bold on; pattern: pattern solid, fore_colour gray25;align:horizontal left, indent 1,vertical center" )
        for i, fieldname in enumerate( fields ):
            worksheet.write( 0, i, fieldname, header_title )
            worksheet.col( i ).width = 8000  # around 220 pixels
        base_style = xlwt.easyxf( 'align: horizontal left,wrap yes,indent 1,vertical center' )
        date_style = xlwt.easyxf( 'align: horizontal left,wrap yes, indent 1,vertical center', num_format_str='YYYY-MM-DD' )
        datetime_style = xlwt.easyxf( 'align: horizontal left,wrap yes,indent 1,vertical center', num_format_str='YYYY-MM-DD HH:mm:SS' )
        worksheet.row( 0 ).height = 400
        for row_index, row in enumerate( rows ):
            worksheet.row( row_index + 1 ).height = 350
            for cell_index, cell_value in enumerate( row ):
                cell_style = base_style
                if isinstance( cell_value, basestring ):
                    cell_value = re.sub( "\r", " ", cell_value )
                elif isinstance( cell_value, datetime.datetime ):
                    cell_style = datetime_style
                elif isinstance( cell_value, datetime.date ):
                    cell_style = date_style
                worksheet.write( row_index + 1, cell_index, cell_value, cell_style )
        fp = StringIO()
        workbook.save( fp )
        fp.seek( 0 )
        data = fp.read()
        fp.close()
        return data

    @api.multi
    def export_with_domain( self ):
        context = dict( self._context ) or {}
        e_data = {}
        line_fields = []
        if self.export_fields :
            rexport_fields_sorted = self.export_fields.sorted( key=attrgetter( 'sequence', 'heading', 'name' ) )  # export_obj.export_fields.sorted(key=lambda r: r.sequence)
            field_names = map( lambda x:x.name, rexport_fields_sorted )
            field_headings = map( lambda x:x.heading, rexport_fields_sorted )
            export_data = []
            domain = []
            if self.domain :
                domain = eval( self.domain )
            record_ids = self.env[ self.resource ].search( domain )
            if record_ids :
                export_data = record_ids.export_data( field_names, True ).get( 'datas', [] )
                data = base64.encodestring( self.from_data( field_headings, export_data ) )
                attach_vals = {
                         'name':'%s.xls' % ( self.resource ),
                         'datas':data,
                         'datas_fname':'%s.xls' % ( self.resource ),
                         }

                doc_id = self.env['ir.attachment'].create( attach_vals )
                if self.attachment_id :
                    try :
                        self.attachment_id.unlink()
                    except :
                        pass
                self.write( {'attachment_id':doc_id.id} )
                return {
                    'type' : 'ir.actions.act_url',
                    'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=name&id=%s' % ( doc_id.id ),
                    'target': 'self',
                    }


    @api.multi
    def export_old_file( self ):
        if self.attachment_id :
            return {
                'type' : 'ir.actions.act_url',
                'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=name&id=%s' % ( self.attachment_id.id ),
                'target': 'self',
                }

        else:
            raise osv.except_osv( _( 'Attachment not found !' ), _( 'There is no last export for this record.' ) )

    @api.multi
    def export_and_send( self ):
        assert len( self._ids ) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.env['ir.model.data']
        if self.attachment_id :
            try:
                template_id = ir_model_data.get_object_reference( 'ir_export_extended_ept', 'email_template_export_with_domain_ept' )[1]
            except ValueError:
                template_id = False
            try:
                compose_form_id = ir_model_data.get_object_reference( 'mail', 'email_compose_message_wizard_form' )[1]
            except ValueError:
                compose_form_id = False
            ctx = dict()
            ctx.update( {
                        'default_model': 'ir.exports',
                        'default_attachment_ids': [( 6, 0, [self.attachment_id.id] )],
                        'default_res_id': self._ids[0],
                        'default_use_template': bool( template_id ),
                        'default_template_id': template_id,
                        'default_composition_mode': 'comment',
                        'mark_so_as_sent': True
                        } )

            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [( compose_form_id, 'form' )],
                'view_id': compose_form_id,
                'target': 'new',
                'context': ctx,
                }
        else:
            raise Warning( _( """There is no file found for attachment. Please click on "Export Data" button and select the option "Latest and Save".""" ) )


