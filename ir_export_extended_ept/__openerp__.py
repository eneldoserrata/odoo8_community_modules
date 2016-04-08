{
    'name': 'Export data in Excel',
    'summary' : 'Manage export list with custom domain,export them to Excel & email it',
    'version': '1.0',
    'category': 'Extra Tools',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    'complexity': "normal",
    'sequence': 20,
    'description': """
By default in Odoo when you save your custom export, system hasn't any view for that to use those custom defined export list. \n
After installation of this module you can see your custom defined export list from the menu Reporting >> Export Data >> Export. \n
You can see all your custom defined exports over there. You can apply domain, change the sequence of fields, add more fields to export, add your Custom headers and export data to Excel file. \n
You can also email that export file to your customers directly from Odoo. \n

Feel free to contact us at info@emiprotechnologies.com for more customisations in Odoo. \n

Visit below link to find our more cool apps to shape your system ! \n

https://www.odoo.com/apps/modules?author=Emipro%20Technologies%20Pvt.%20Ltd. \n
""",
    'depends': [
                'base', 'email_template', 'web'
                ],
    'data': ['data/export_data_templates.xml',
             'view/ir_exports.xml',
             'view/ir_exports_line.xml',
             'wizard/export_wizard_view.xml',
             'view/webclient_templates.xml',
            ],

    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/main_screen.png'],
}
