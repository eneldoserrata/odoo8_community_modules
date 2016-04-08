# -*- coding: utf-8 -*-
{
    "name" : "Pricelist by Payment Term",
    "version" : "0.1",
    "author" : "Grupo CITEC",
    "category": 'CITEC Plugins',
    'complexity': "easy",
    "description": """
Pricelist by Payment Term
====================================
This module associates Pricelists with Payment Terms. If set, on sales
orders/Quotations, the corresponding Pricelist will be selected
when a Payment Term is selected.

for OpenERP 7.0

Programado pelo Grupo CITEC Ltda.
http://www.grupocitec.com
v0.1
    """,
    'website': 'http://www.grupocitec.com',
    "depends" : [
    	"base", 
    	"sale", 
    	"account", 
	],
    'init_xml': [],
    'update_xml': [
    	"view/sale_view.xml", 
    	"view/account_view.xml", 
    ],
    'data': [
    ],
    'demo_xml': [],
    'test': [],
    'application': False,
    'installable': True,
    'css': [
    ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
