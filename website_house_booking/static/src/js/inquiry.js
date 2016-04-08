            $( document ).ready(function() {
                $('.calendar').calendar({
                    'fetch': false,
                    'numberOfMonths': [1,3],
                    "calendar": {
                        "range": {
                            "startDate": '2013-02-12',
                            "endDate": '2013-02-15',
                            "reservationId": "inquiry"
                        },
                        "2013-02-11": {
                            "status": "RESERVE",
                            "reservationId": "1"
                        },
                        "2013-02-12": {
                            "status": "RESERVE",
                            "reservationId": "1"
                        },
                        "2013-02-13": {
                            "status": "RESERVE",
                            "reservationId": "1"
                        },
                    },
                    "reservations": {
                        "inquiry": {
                            "status": "INQUIRY"
                        },
                        "1": {
                            "checkinDate": "2013-02-11",
                            "checkoutDate": "2013-02-14",
                            "checkinTime": "01:30",
                            "checkoutTime": "21:00",
                            "status": "RESERVE"
                        },
                    },
                    'defaultDate': '2013-01-01'
                });
            });