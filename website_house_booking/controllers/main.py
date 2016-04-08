# -*- coding: utf-8 -*-

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp import SUPERUSER_ID

from datetime import date, timedelta


def str2date(s):
    return date(*map(int, s.split('-')))


def date2str(d):
    return str(d)[:10]


def check_dates(values):
    arrival_day = values.get("arrival_day")
    departure_day = values.get("departure_day")
    error = set()
    if arrival_day is not None and arrival_day < str(date.today()):
        values["arrival_day"] = None
        values["departure_day"] = None
        error.add("arrival_day")
    if departure_day is not None and departure_day < arrival_day:
        values["departure_day"] = None
        error.add("departure_day")
    return values, error


def inject_calendar_values(values, booking_model, nb_month=3, context=None):
    # Adapt for 1-month calendar or 3-month calendar

    if context is None:
        context = {}
    values['lang'] = context.get('lang')

    if nb_month == 3:
        delta_start = -30
        delta_stop = 60
    else:
        delta_start = 0
        delta_stop = 30

    # arrival_day may not exist if the booking process is not started
    if values.get("arrival_day") is None:
        start_day = str(date.today())
    else:
        start_day = values["arrival_day"]
    # Get start day for the calendar
    values["today"] = str(date(*map(int, start_day.split("-"))))
    values["start_day"] = start_day =\
        str(date(*map(int, start_day.split("-")))
            + timedelta(days=delta_start))[:8] + "01"
    # Add it to the domain
    domain = [("departure_day", ">", start_day)]

    # departure_day may not exist if the booking process is not started
    # if so, we look oll future reservations.
    if values.get("departure_day") is not None:
        # Get stop day for the calendar : add two month, get the first day
        stop_day = str(date(*map(int, values['departure_day'].split('-'))) +
                       timedelta(days=delta_stop))[:8] + "01"
        # back one day
        stop_day = str(date(*map(int, stop_day.split('-')))
                       + timedelta(days=-1))[:10]
        domain .append(('arrival_day', '<', stop_day))

    # Get all bookings related to these dates
    booking_ids = booking_model.search(
        request.cr,
        SUPERUSER_ID,
        domain,
        context=request.context)

    # Read those records
    values['reservations'] = booking_model.read(
        request.cr,
        SUPERUSER_ID,
        booking_ids,
        ['id', 'departure_day', 'arrival_day'],
        context=request.context)
    days = []
    for r in values['reservations']:
        start, stop = map(str2date, (r['arrival_day'], r['departure_day']))
        current_id = r['id']
        while start < stop:
            days.append((date2str(start), current_id))
            start += timedelta(days=1)
    values['reservedays'] = days
    return values




class booking(http.Controller):

    @http.route(
        ['/booking'],
        type='http',
        auth='public',
        website=True,
        multilang=True)
    def booking(
        self, name=None, company=None, arrival_day=None, departure_day=None,
        persons_number=None, street=None, street2=None, zipcode=None, city=None,
        phone=None, email=None
    ):

        # Useful Models
        partner_model = request.registry['res.partner']
        booking_model = request.registry['house_booking.booking']

        # Getting all values
        values = locals().copy()
        del values['self']

        # Check dates
        values, error = check_dates(values)

        # Mandatory fields set:
        required_fields = ['name',
                           'arrival_day',
                           'departure_day',
                           'persons_number',
                           'phone',
                           'email',
                           'street',
                           'zipcode',
                           'city',
                           ]

        # Check mandatory fields
        for field in required_fields:
            if not values.get(field):
                error.add(field)
        if error:
            values = inject_calendar_values(
                values, booking_model, nb_month=1, context=request.context)
            return request.website.render(
                "website_house_booking.booking_form", values)

        # Initialize mappings
        post_partner = {}
        post_booking = {}
        post_company = {}

        # Partner stuff
        post_partner["lang"] = request.context.get("lang", "fr_FR")
        post_partner['name'] = name
        post_partner['phone'] = phone
        post_partner['email'] = email
        post_partner['user_id'] = False  # Salesman field is empty
        # Booking stuff
        post_booking['arrival_day'] = arrival_day
        post_booking['departure_day'] = departure_day
        post_booking['persons_number'] = persons_number

        # If partner is a company, address is related to the company
        if company:
            # Company stuff
            post_company['name'] = company
            post_company['street'] = street
            post_company['street2'] = street2
            post_company['zipcode'] = zipcode
            post_company['city'] = city
            post_company['is_company'] = True
            # Create now the company  (and update partner) !
            post_partner['parent_id'] = partner_model.create(
                request.cr,
                SUPERUSER_ID,
                post_company,
                context=request.context)
            # Partner stuff
            post_partner['use_parent_address'] = True
            # Booking stuff
            post_booking['name'] = ' - '.join([name, company])
        else: # Otherwise, the address is related to the partner.
            # Partner stuff
            post_partner['name'] = company
            post_partner['street'] = street
            post_partner['street2'] = street2
            post_partner['zipcode'] = zipcode
            post_partner['city'] = city
            # Booking stuff
            post_booking['name'] = name

        # Searching the current partner
        partner_search = partner_model.search(
            request.cr,
            SUPERUSER_ID,
            [('email', '=', post_partner['email'])],
            context=request.context)

        if partner_search:  # If the partner already exists, we update new data
            post_booking['partner_id'] = partner_search[0]
            partner_model.write(
                request.cr,
                SUPERUSER_ID,
                partner_search,
                post_partner)
        else:  # Otherwise, a new partner is created
            post_booking['partner_id'] = partner_model.create(
                request.cr,
                SUPERUSER_ID,
                post_partner,
                context=request.context)

        # We now check if the booking can be made
        if booking_model.check_availability(
            request.cr,
            SUPERUSER_ID,
            arrival_day,
            departure_day,
            context=request.context
        ):

            # We book
            booking_model.create(
                request.cr,
                SUPERUSER_ID,
                post_booking,
                context=request.context)
            return request.website.render(
                "website_house_booking.booking_thanks",
                values)

        else: # We propose to change dates
            values['partner_id'] = post_booking['partner_id']
            values = inject_calendar_values(values, booking_model, context=request.context)
            return request.website.render(
                "website_house_booking.booking_changedate",
                values)




    @http.route(
        ['/booking/dates'],
        type='http',
        auth='public',
        website=True,
        multilang=True)
    def booking_changedate(self, **values):

        values, error = check_dates(values)

        # Useful Models
        booking_model = request.registry['house_booking.booking']

        mandatory_keys = (
            "name",
            "persons_number",
            "arrival_day",
            "departure_day",
            "partner_id",
            )

        # Check mandatory keys (hidden fields)
        for key in mandatory_keys :
            if not values.get(key):
                error.add(key)

        if error:
            values = inject_calendar_values(
                values, booking_model, context=request.context)
            values['error'] = error
            return request.website.render(
                "website_house_booking.booking_changedate", values)

        if not booking_model.check_availability(
            request.cr,
            SUPERUSER_ID,
            values['arrival_day'],
            values['departure_day'],
            context=request.context
        ):

            values = inject_calendar_values(
                values, booking_model, context=request.context)
            return request.website.render(
                "website_house_booking.booking_changedate", values)

        # We book
        booking_model.create(
            request.cr,
            SUPERUSER_ID,
            values,
            context=request.context)
        return request.website.render(
            "website_house_booking.booking_thanks", values)

