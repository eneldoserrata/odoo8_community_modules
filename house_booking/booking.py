# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _

import operator


class Booking(osv.Model):
    """Main model"""

    _name = "house_booking.booking"

    _description = "booking"

    _inherit = ['mail.thread']

    _states = [
        ('pending', "Pending"),
        ('approved', "Approved"),
        ('denied', "Denied"),
    ]

    def _get_deposit(self, cr, uid, ids, field, arg, context=None):
        """Deposit"""
        # TODO: Refaire la lecture de la configuration.
        # TODO: Refaire en pythonique
        setting_obj = self.pool.get('booking.config.settings')
        config_ids = setting_obj.search(cr, uid, [], limit=1, order='id DESC', context=context)
        if config_ids:
            deposit = setting_obj.read(cr, uid, config_ids[0], ['deposit'], context=context)['deposit']
        else:
            deposit = 0
        res = {}
        for reserv in self.browse(cr, uid, ids, context=context):
            if reserv.price > 0:
                res[reserv.id] = deposit
        return res

    def _get_advance_ratio(self, cr, uid, ids, field, arg, context=None):
        """Advance Payment ratio"""
        # TODO: Refaire la lecture de la configuration.
        # TODO: Refaire en pythonique
        setting_obj = self.pool.get('booking.config.settings')
        config_ids = setting_obj.search(cr, uid, [], limit=1, order='id DESC', context=context)
        if config_ids:
            advance_payment = setting_obj.read(cr, uid, config_ids[0], ['advance_payment'], context=context)['advance_payment']
        else:
            advance_payment = 0
        res = {}
        for reserv in self.browse(cr, uid, ids, context=context):
            res[reserv.id] = advance_payment
        return res

    def _get_advance_payment(self, cr, uid, ids, field, arg, context=None):
        """Advance Payment depending on price"""
        # TODO: Refaire la lecture de la configuration.
        # TODO: Refaire en pythonique
        setting_obj = self.pool.get('booking.config.settings')
        config_ids = setting_obj.search(cr, uid, [], limit=1, order='id DESC', context=context)
        if config_ids:
            advance_payment = setting_obj.read(cr, uid, config_ids[0], ['advance_payment'], context=context)['advance_payment']
        else:
            advance_payment = 0
        res = {}
        for reserv in self.browse(cr, uid, ids, context=context):
            if reserv.price > 0:
                res[reserv.id] = int(round(reserv.price*advance_payment/100, -2))
            else:
                res[reserv.id] = 0
        return res

    def _get_balance_due(self, cr, uid, ids, field, arg, context=None):
        """Return the difference between total price and advance payment"""
        # TODO: Refaire la lecture de la configuration.
        # TODO: Refaire en pythonique
        setting_obj = self.pool.get('booking.config.settings')
        config_ids = setting_obj.search(cr, uid, [], limit=1, order='id DESC', context=context)
        if config_ids:
            advance_payment = setting_obj.read(cr, uid, config_ids[0], ['advance_payment'], context=context)['advance_payment']
        else:
            advance_payment = 0
        res = {}
        for reserv in self.browse(cr, uid, ids, context=context):
            if reserv.price > 0:
                res[reserv.id] = int(reserv.price - round(reserv.price*advance_payment/100, -2))
            else:
                res[reserv.id] = 0
        return res
        res = {}

    def _get_title(self, cr, uid, ids, field, arg, context=None):
        """Return the reservation title"""
        # TODO: Refaire la lecture de la configuration.
        # TODO: Refaire en pythonique
        # TODO: Le titre doit être traductible.
        setting_obj = self.pool.get('booking.config.settings')
        config_ids = setting_obj.search(cr, uid, [], limit=1, order='id DESC', context=context)
        if config_ids:
            booking_title = setting_obj.read(cr, uid, config_ids[0], ['booking_title'], context=context)['booking_title']
        else:
            booking_title = ""
        res = {}
        for reserv in self.browse(cr, uid, ids, context=context):
            res[reserv.id] = booking_title
        return res

    def _date_to_datetime(self, cr, uid, ids, field, arg, context=None):
        """Convert date to datetime (with rules for arrival and departure)"""
        # TODO: Refaire en pythonique
        if field == 'arrival_date':
            f, h = operator.attrgetter('arrival_day'), " 16:00:00"
        else:  # departure_date
            f, h = operator.attrgetter('departure_day'), " 10:00:00"

        result = {b.id: f(b) + h for b in self.browse(cr, uid, ids, context=context)}

        return result

    _columns = {
        'name': fields.char(
            'Title',
            size=256,
            required=True,
            select=True,
        ),
        'arrival_day': fields.date(
            string="Arrival day",
            required=True,
        ),
        'arrival_date': fields.function(
            _date_to_datetime,
            type='datetime',
            string="Arrival date",
            store=True,
        ),
        'departure_day': fields.date(
            string="Departure day",
            required=True,
        ),
        'departure_date': fields.function(
            _date_to_datetime,
            type='datetime',
            string="Departure date",
            store=True,
        ),
        'persons_number': fields.integer(
            string="Number of Persons",
        ),
        'partner_id': fields.many2one(
            'res.partner',
            string="Client",
            required=True,
        ),
        'state': fields.selection(
            _states,
            string="Booking's state",
        ),
        'price': fields.integer(
            string="Price of booking",
        ),
        'advance_payment': fields.function(
            _get_advance_payment,
            type='integer',
            string="Advance payment",
            store=True,
        ),
        'balance_due': fields.function(
            _get_balance_due,
            type='integer',
            string="Balance due",
            store=True,
        ),
        'advance_ratio': fields.function(
            _get_advance_ratio,
            type='integer',
            string="Advance Ratio",
            store=True,
        ),
        'deposit': fields.function(
            _get_deposit,
            type='integer',
            string="Deposit",
            store=True,
        ),
        'voucher_title': fields.function(
            _get_title,
            type='char',
            string="Voucher's title",
            store=True,
        ),
    }

    _order = 'create_date desc'

    _defaults = {
        'state': 'pending',
    }

    _sql_constraints = [
        (
            "house_booking_arrival_before_departure_date_constraint",
            "CHECK(arrival_date < departure_date)",
            "'Arrival date' should be before 'Departure date'",
        ),
        (
            "house_booking_arrival_before_departure_day_constraint",
            "CHECK(arrival_day < departure_day)",
            "'Arrival day' should be before 'Departure day'",
        ),
    ]

    def create(self, cr, uid, values, context=None):
        """
        Check availability before creating.
        """
        arrival_date, departure_date, = values['arrival_day'] + " 16:00:00", values['departure_day'] + " 10:00:00"
        if not self.check_availability(cr, uid, arrival_date, departure_date, context=context):
            raise osv.except_osv(_('Unavailable dates !'), _("Unable to book for the selected dates."))
        return osv.Model.create(self, cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        """
        Check availability before writing.
        """
        # Can't change many booking dates at once.
        if type(ids) == list and len(ids) > 1 and ('arrival_date' in values or 'departure_date' in values):
            raise osv.except_osv(('Date Change denied !'), ("Changing departure or arrival dates for several bookings at the same time is not allowed."))
        elif type(ids) != list:
            ids = [ids]

        arrival_date, departure_date = None, None

        # Get the two dates (if it is true, we are sure that there is one and only one id in 'ids')
        if 'arrival_day' in values and 'departure_day' not in values:
            read = self.read(cr, uid, ids[0], ['departure_date'], context=context)
            arrival_date, departure_date = values['arrival_day'] + " 16:00:00", read['departure_date']
        elif 'departure_day' in values and 'arrival_day' not in values:
            read = self.read(cr, uid, ids[0], ['arrival_date'], context=context)
            arrival_date, departure_date = read['arrival_date'], values['departure_day'] + " 10:00:00"

        if arrival_date is not None: # departure_date is not None too !
            # Checking available periods. (if it is true, we are sure that there is one and only one id in 'ids')
            if not self.check_availability(cr, uid, arrival_date, departure_date, current_id=ids[0], context=context):
                raise osv.except_osv(('Unavailable dates !'), ("Unable to book for the selected dates."))

        # self.message_post(cr, uid, ids, _('Booking <b>updated</b>'), context=context)

        return osv.Model.write(self, cr, uid, ids, values, context=context)

    def accept_booking(self, cr, uid, ids, context=None, *args):
        """
        Change state to 'approved'.
        """
        if type(ids) != list:
            ids = [ids]
        read = self.read(cr, uid, ids, ['price'], context=context)
        if any(r['price'] <= 0 for r in read):
            raise osv.except_osv(_('Price not set !'), _("Booking price has to be set."))
        self.write(cr, uid, ids, {'state': 'approved'})
        self.message_post(cr, uid, ids, _('Booking <b>approved</b>'), context=context)
        
        self.send_email(cr, uid, ids, context=context)   
        return True
    
    
    def send_email(self, cr, uid, ids, context=None):
        """Send email"""
        template_id = self.pool.get('email.template').search(cr, uid, [('name', '=', 'House booking - Send by Email')], context=context)[0]
        email_obj = self.pool.get('email.template')
        email_obj.send_mail(cr, uid, template_id, ids[0], force_send=True)
    
    def refuse_booking(self, cr, uid, ids, context=None, *args):
        """
        Change state to 'denied'.
        """
        self.write(cr, uid, ids, {'state': 'denied'})
        self.message_post(cr, uid, ids, _('Booking <b>denied</b>'), context=context)
        return True

    def check_availability(self, cr, uid, arrival_date, departure_date, current_id=None, context=None):
        """
        Return True if all dates between arrival_date and departure_date are available, False otherwise.
        """
        # sch : supprimé au 15 mai
        #if len(arrival_date) == 10:
        #    arrival_date += " 16:00:00"
        #if len(departure_date) == 10:
        #    departure_date += " 16:00:00"
        # Domain of bookings crossing targeted period.
        domaine = [
            ('state', '!=', 'denied'),
            '!',
            '|',
            ('arrival_date','>=',departure_date),
            ('departure_date','<=',arrival_date),
        ]
        
        sch = self.search(cr, uid, [], context=context)
        brw = self.browse(cr, uid, sch, context=context)

        # Remove current booking.
        if current_id is not None:
            domaine.insert(0, ('id', '!=', current_id))

        search = self.search(cr, uid, domaine, context=context)
        long = len(search)
        res = long == 0
        return res
