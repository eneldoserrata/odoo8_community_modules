# -*- coding: utf-8 -*-

{
    'name' : 'Booking management',
    'version' : '1.2',
    'author' : 'Alicia FLOREZ & Sébastien CHAZALLET',
    'category': 'Sales Management',
    'summary': 'Management of house, guestroom or hotel bookings.',
    'description' : """
Manage your bookings
====================

This module is used by :

- hotels
- guest houses
- guest rooms

Manage rental schedule, bookings, arrivals and departure.

Use it with its WebSite App and allow your customers to rent online !

    In further versions, will manage quotations, invoices, and seasons.
""",
    'website': 'http://www.inspyration.fr',
    'images' : [],
    'depends' : ['base', 'mail', 'crm'],
    'data': [
        'security/booking_security.xml',
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'views/booking_view.xml',
        'report/voucher.xml',
        'views/email.xml',
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
