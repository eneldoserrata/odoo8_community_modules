(function() {
    var web_action_request = openerp.web_action_request = {};

    web_action_request.Request = openerp.Widget.extend({
        init: function(parent, user_id) {
            var self = this;
            this._super(parent);
            this.bus = openerp.bus.bus;
            this.channel = 'action.request_' + user_id;
            this.bus.add_channel(this.channel);
            this.bus.on("notification", this, this.on_notification);
            this.bus.start_polling();
        },
        on_notification: function(notification) {
            var self = this;
            var channel = notification[0];
            if (channel == this.channel) {
                var action = notification[1];
                openerp.client.action_manager.do_action(action);
            }
        },
    });
    openerp.web.WebClient.include({
        show_application: function() {
            this._super();
            this.web_action_request = new web_action_request.Request(this, this.session.uid);
        },
    });
})();
