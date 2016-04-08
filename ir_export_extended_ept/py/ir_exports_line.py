from openerp import models, fields

_FIELD_LIST = [( '', '' )]
class ir_exports_line( models.Model ):
    _name = "ir.exports.line"
    _inherit = "ir.exports.line"
    _order = "sequence"

    def get_fields( self ):
        return []

    heading = fields.Char( string="Label", size=512 )
    sequence = fields.Integer( 'Sequence' )
