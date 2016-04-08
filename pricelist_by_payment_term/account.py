# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round

import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class account_payment_term(osv.osv):
    _name = "account.payment.term"
    _inherit = "account.payment.term"
    _columns = {
        'pricelist_id': fields.many2one('product.pricelist', 'Default Pricelist'),
    }

account_payment_term()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
