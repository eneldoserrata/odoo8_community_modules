from openerp import models, fields

class base_config_settings(models.TransientModel):
    _inherit = 'base.config.settings'
    
    group_visible_outgoing_mail_per_user = fields.Boolean( 'Send Userwise Outgoing emails?',
                        implied_group='base.group_outgoing_mail_per_user',                                     
                        help = 'You can allow user to set user in Outgoing server.')
