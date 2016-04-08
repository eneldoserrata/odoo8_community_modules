from openerp import models, api


class ActionRequest(models.AbstractModel):
    _name = 'action.request'
    _description = 'Action Request'

    @api.model
    def notify(self, action):
        self.env['bus.bus'].sendone('%s_%d' % (self._name, self.env.uid),
                                    action)
