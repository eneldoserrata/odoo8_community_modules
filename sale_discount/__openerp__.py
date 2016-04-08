# -*- coding: utf-8 -*-

{
    'name': 'Sale Discount',
    'version': '1.0',
        'sequence': 1,
    'category': 'Sales Management',
    'summary': 'Show discount total and total before discount on sales orders.',
    'description':"Show Discount Total and Total before Discount on Sales Orders.",
    'author': 'M.Hagag@DVIT.ME',
    'website': 'https://www.dvit.me',
    'depends': ['sale','invoice_discount'],
    'data': ['discount_view.xml',
             'views/report_discount.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
