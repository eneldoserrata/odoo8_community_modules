from openerp import models, fields, api

class export_wizard(models.TransientModel):
    _name='export.wizard.ept'    
    export_version=fields.Selection([('last_one','Last One'),('latest_save','Latest and Save')],"Export Version",default='latest_save')                 
             
    @api.multi
    def download_file(self):
        context=dict(self._context) or {}
        if context and context.get('active_id',False):
            export_id = context.get('active_id',False)
            export = self.env['ir.exports']
            export_obj=export.browse(export_id)
            version=self.read(['export_version'])
            print version
            if version[0]['export_version']=='latest_save':
                res=export_obj.export_with_domain()
            else:
                res=export_obj.export_old_file()
            return res
