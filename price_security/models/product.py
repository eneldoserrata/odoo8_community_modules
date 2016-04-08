# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _

class product_template(models.Model):
    _inherit = 'product.template'

    can_modify_prices = fields.Boolean(
        help=_('If checked all users can modify the\
        price of this product in a sale order or invoice.'),
        string=_('Can modify prices'))
