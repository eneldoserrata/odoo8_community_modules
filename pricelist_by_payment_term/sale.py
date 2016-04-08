# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    def onchange_payment_term(self, cr, uid, ids, payment_term_id, context=None):
        v = {}
        if payment_term_id:
            payment_term = self.pool.get('account.payment.term').browse(cr, uid, payment_term_id, context=context)
            if payment_term and payment_term.pricelist_id and payment_term.pricelist_id.id:
                v['pricelist_id'] = payment_term.pricelist_id.id
        return {'value': v}

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
