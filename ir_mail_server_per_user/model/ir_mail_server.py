from openerp.osv import osv, fields
from openerp import SUPERUSER_ID

class ir_mail_server(osv.Model):
    _inherit = "ir.mail_server"
    _columns = {
                'user_id_ept' : fields.many2one('res.users','User',help='When user is assigned then at the time of email sending from Odoo if no outgoing server found then \
                                    system will take the server which is assigned to this user.')
    }              
    def send_email(self, cr, uid, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,context=None):
        ctx = context and context.copy() or {}
        mail_server = mail_server_id
        user_id = ctx.get('ept_user_id')
        if not mail_server and user_id:
            user_obj = self.pool.get('res.users').browse(cr,uid,user_id)
            email = user_obj.partner_id and user_obj.partner_id.email or False
            if email :
                mail_server_ids = self.search(cr,SUPERUSER_ID,[('user_id_ept','=',user_id)], order='sequence', limit=1)
                if mail_server_ids :
                    mail_server = mail_server_ids[0]
        return super(ir_mail_server,self).send_email(cr,uid,message,mail_server_id=mail_server)
    