(function() {
    'use strict';

    var website = openerp.website;

    website.snippet.options.custom_snippet_tabs = openerp.website.snippet.Option.extend({

        start: function() {
            var self = this;

            this.$el.find(".js_add").on("click", _.bind(this._add_new_tab, this));
            this.$el.find(".js_remove").on("click", _.bind(this._remove_current_tab, this));

            this._super();
        },

        drop_and_build_snippet: function() {
            var self = this;
            var unique_id = Math.random().toString(36).substring(7);
            self.$target.find('.nav-tabs > li > a').each(function() {
                var item = $(this);
                var href = item.attr('href');
                item.attr('href', String(href) + String(unique_id));
                item.attr('data-cke-saved-href', String(item.attr('data-cke-saved-href')) + String(unique_id));
                item.attr('aria-controls', String(item.attr('aria-controls')) + String(unique_id));
                var pane = self.$target.find('.tab-content > div' + href);
                pane.attr('id', String(pane.attr('id')) + String(unique_id))
            });
        },

        _add_new_tab: function() {
            var self = this;
            var tabs = self.$target.find('.nav-tabs');
            var panes = self.$target.find('.tab-content');
            var newid = Math.random().toString(36).substring(7);

            var li = $('<li/>', {
                'role': 'presentation',
                'class': 'active'
            });
            $('<a/>', {
                'href': '#' + newid,
                'aria-controls': 'tab1',
                'role': 'tab',
                'data-toggle': 'tab',
                'text': 'New'
            }).appendTo(li);

            var div = $('<div/>', {
                'role': 'tabpanel',
                'class': 'oe_structure oe_empty tab-pane active',
                'id': newid
            });

            li.insertBefore(tabs.find('.active').removeClass('active'));
            div.insertBefore(panes.find('.active').removeClass('active'));
        },

        _remove_current_tab: function() {
            var self = this;
            var tabs = self.$target.find('.nav-tabs');
            var panes = self.$target.find('.tab-content');

            if (tabs.find('> li[role="presentation"]').size() > 1 && panes.find('> div[role="tabpanel"]').size() > 1) {
                tabs.find('.active').remove();
                panes.find('.active').remove();
                tabs.find('> li[role="presentation"]:first').addClass('active');
                panes.find('> div[role="tabpanel"]:first').addClass('active');
            }
        },
    });

})();