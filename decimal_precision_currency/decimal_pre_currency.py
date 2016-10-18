# coding: utf-8
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Maria Gabriela Quilarque  <gabriela@openerp.com.ve>
#    Planified by: Nhomar Hernandez <nhomar@vauxoo.com>
#    Audited by: Maria Gabriela Quilarque  <gabriela@openerp.com.ve>
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

from openerp.osv import fields, osv
from openerp import fields as fields2, _

import time
import openerp.addons.decimal_precision as dp


class ResCurrencyRate(osv.Model):

    _inherit = "res.currency.rate"
    _columns = {
        'rate': fields.float('Rate',
                             digits_compute=dp.get_precision('Currency'), required=True,
                             help='The rate of the currency to the currency of rate 1'),
    }


class ResCurrency(osv.Model):

    def _current_rate(self, cr, uid, ids, name, arg, context=None):
        return self._get_current_rate(cr, uid, ids, context=context)

    def _get_current_rate(self, cr, uid, ids, raise_on_no_rate=True, context=None):
        if context is None:
            context = {}
        res = {}

        date = fields2.Datetime.now()
        if context.get('date', False):
            date = "{}".format(context.get('date').split(" ")[0])

        for id in ids:

            query = "SELECT rate FROM res_currency_rate WHERE currency_id = {} AND name = '{}' ORDER BY name desc LIMIT 1".format(
                id, date)

            cr.execute(query)

            if cr.rowcount:
                res[id] = cr.fetchone()[0]
            elif not raise_on_no_rate:
                res[id] = 0
            else:
                if id != 74:
                    currency = self.browse(cr, uid, id, context=context)
                    raise osv.except_osv(_('Advertencia!'),_("No hay tasa de cambio asociado de la moneda '%s' para la fecha de la factura" % (currency.name)))
                else:
                    res[id] = 1
        return res


    _inherit = "res.currency"
    _columns = {
        'rate': fields.function(_current_rate, method=True,
                                string='Current Rate', digits_compute=dp.get_precision('Currency'),
                                help='The rate of the currency to the currency of rate 1'),
        'rounding': fields.float('Rounding factor',
                                 digits_compute=dp.get_precision('Currency')),

    }
