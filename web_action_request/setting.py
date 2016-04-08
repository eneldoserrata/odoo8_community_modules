from openerp import models, fields, api


class Setting(models.TransientModel):
    _name = 'web.action.request.setting'
    _description = 'test the request'
    _inherit = 'res.config.settings'

    action = fields.Many2one('ir.actions.act_window', required=True)
    user = fields.Many2one('res.users', default=lambda self: self.env.user,
                           required=True)

    @api.multi
    def button_check_action_request(self):
        action = self.action.read()[0]
        self.sudo(self.user.id).env['action.request'].notify(action)
        return True
