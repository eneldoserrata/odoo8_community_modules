# -*- coding: utf-8 -*-
from openerp.osv import osv

class mail_notification(osv.Model):
    """ Class holding notifications pushed to partners. Followers and partners
        added in 'contacts to notify' receive notifications. """
    _inherit = 'mail.notification'
    
    def _notify(self, cr, uid, message_id, partners_to_notify=None, context=None,
                force_send=False, user_signature=True):
        ctx = context and context.copy() or {}
        ctx.update({'ept_user_id':uid})    
        return super(mail_notification,self)._notify(cr,uid,message_id,partners_to_notify,ctx,force_send,user_signature) 
