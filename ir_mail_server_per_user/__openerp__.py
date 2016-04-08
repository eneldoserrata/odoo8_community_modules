{
    'name': 'Outgoing Email Extension',
    'summary' : 'Configure userwise outgoing email server',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    'category': 'Social Network',
    'version': '1.0',
    'description':
        """
By default in Odoo, when email goes out from system and if no outgoing mail server specified, it selects the outgoing server which is having low priority. \n

From any user if you try to send email, system will select only one lowest prioritised outgoing server. \n

After installation of this module, you can configure user wise outgoing server. So it will be possible to send user wise outgoing emails from Odoo.
        
==================================================================== \n

For support on this module contact us at info@emiprotechnologies.com \n

To subscribe our support packages, visit following link, \n

http://www.emiprotechnologies.com/odoo/support \n 

Visit following link to find our other cool apps to shape your system . \n

https://www.odoo.com/apps/modules?author=Emipro%20Technologies%20Pvt.%20Ltd. \n

For more information about us, visit www.emiprotechnologies.com \n
        """,
    'depends': ['mail'],
    'data': [
             'security/security_group.xml',
             'view/ir_mail_server_view.xml',
             'view/res_config.xml',
             ],
    'images': ['static/description/main_screen.png'],
    "installable": True,
    "auto_install": False,
    'application' : True,
}
