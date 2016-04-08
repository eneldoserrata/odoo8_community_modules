# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author: Frank Carvajal. Copyright ClearCorp SA
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

from openerp.osv import osv, fields
#from tools import debug

class account_journal(osv.osv):
	_name = "account.journal"
	_inherit = "account.journal"
	_columns = {
		
		'payment_method_customer'   : fields.boolean('Forma de Pago del Cliente?'),
		'payment_method_supplier'   : fields.boolean('Forma de Pago del Proveedor?'),
		'payment_verification'      : fields.boolean('Verificación de Pago?'),
		'active': fields.boolean('Activo?'),
		
	}
	
	_defaults = {
		'active': True,
	}
	
account_journal()
