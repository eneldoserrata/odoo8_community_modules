# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Ursa Information Systems, Adam O'Connor, Balaji Kannan
#    Copyright 2015
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{'name' : 'Ursa Customer Statements',
 'version' : '1.8',
 'author' : 'Ursa Information Systems, Adam O\'Connor, Balaji Kannan',
 'maintainer': 'Ursa Information Systems',
 'category': 'Reporting',
 'complexity': "normal",  # easy, normal, expert
 'depends' : ['base','sale','account'],
 'description': """
  Customer statement report with beginning and ending dates or run by period, etc.
  Supports Version 7 and Version 8.  
""",
 'website': 'http://www.ursainfosystem.com/',
 'init_xml': [],
 'data': ['wizard/account_report_partner_ledger_view.xml', 'wizard/account_report_common_view.xml',],
 'demo_xml': [],
 'tests': [],
 'installable': True,
 'auto_install': False,
 'license': 'AGPL-3',
 'application': False}
