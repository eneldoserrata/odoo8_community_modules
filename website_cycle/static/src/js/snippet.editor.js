(function() {
    'use strict';

    var website = openerp.website;
    
    var cycle_snippet_prefix = 'csc-action-';

    website.snippet.options.custom_snippet_cycle = openerp.website.snippet.Option.extend({

        start : function () {
            var self = this;

            var current_effect = self.$target.attr('data-effect');
            var current_interval = self.$target.attr('data-timeout');

            this.$el.find('a[data-effect="'+current_effect+'"]').parent('li').addClass('active');
            this.$el.find('a[data-timeout="'+current_interval+'"]').parent('li').addClass('active');

            this.$el.find(".js_remove").on("click", _.bind(this._remove_current_image, this));
            this.$el.find(".js_add").on("click", _.bind(this._add_new_image, this));
            this.$el.find(".js_effect").on("click", function(){
                self._add_effect($(this).attr('data-effect'));
            });
            this.$el.find(".js_timeout").on("click", function(){
                self._add_timeout($(this).attr('data-timeout'));
            });
            this._super();
        },

        _add_new_image: function() {
            var self = this;

            var $image = $('<img/>');

            self.element = new CKEDITOR.dom.element($image[0]);
            var editor = new openerp.website.editor.MediaDialog(self, self.element);
            editor.appendTo(document.body);
            editor.$('[href="#editor-media-video"], [href="#editor-media-icon"]').addClass('hidden');

            $image.on('saved', self, function () {
                var src = $image.attr('src');
                var new_image = $('<div/>', {
                    'class' : 'oe_structure',
                    'style': "background: url('" + src + "');"
                });
                if (self.$target.find('.csc-slides').find('.csc-current-slide').size() > 0) new_image.insertAfter(self.$target.find('.csc-slides').find('.csc-current-slide'));
                else self.$target.find('.csc-slides').append(new_image);
                self._reorder();
                self._set_visible(new_image);
            });
            editor.on('cancel', self, function () {
                $image.remove();
            });
        },

        _remove_current_image: function() {
            this.$target.find('.csc-slides').find('.csc-current-slide').remove();
            this.$target.find('.csc-slides').find('div:first').addClass('csc-current-slide');
            this._reorder();
        },

        _add_effect: function(effect) {
            this.$target.attr('data-effect', effect);
            this.$el.find('a[data-effect="'+effect+'"]').parents('ul:first').find('.active').removeClass('active');
            this.$el.find('a[data-effect="'+effect+'"]').parent('li').addClass('active');
        },

        _add_timeout: function(timeout) {
            this.$target.attr('data-timeout', timeout);
            this.$el.find('a[data-timeout="'+timeout+'"]').parents('ul:first').find('.active').removeClass('active');
            this.$el.find('a[data-timeout="'+timeout+'"]').parent('li').addClass('active');
        },

        _reorder: function() {
            var other = this.$target.find('.csc-slides').find('div');
            var i = 0;
            other.each(function() {
                i++;
                if (i == 1) $(this).css({
                    'position': 'absolute',
                    'top': '0px',
                    'z-index': other.size(),
                    'display': 'block',
                    'opacity': 1
                });
                else $(this).css({
                    'position': 'absolute',
                    'top': '0px',
                    'z-index': other.size() - i + 1,
                    'display': 'none',
                    'opacity': 0
                });
            });
        },

        _set_visible: function(element) {
            this.$target.find('.csc-slides').find('div').css({
                'display': 'none',
                'opacity': 0
            }).removeClass('csc-current-slide');

            element.css({
                'display': 'block',
                'opacity': 1
            }).addClass('csc-current-slide');
        }
    });

})();