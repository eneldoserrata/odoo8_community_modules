(function() {
    'use strict';

    var website = openerp.website;

    website.snippet.animationRegistry.custom_snippet_cycle = website.snippet.Animation.extend({
        selector: ".csc",
        start: function () {
            var self = this;
            var effect = self.$target.attr('data-effect');
            var timeout = self.$target.attr('data-timeout');
            var cycle = self.$target.find('.csc-slides');

            cycle.cycle({
                fx: $.inArray(effect, cycle_snippet_effects) > -1 ? effect : 'none',
                next: self.$target.find('.csc-slideshow-right'),
                prev: self.$target.find('.csc-slideshow-left'),
                timeout: (typeof cycle_snippet_intervals[timeout] != "undefined") ? cycle_snippet_intervals[timeout] : 0,
                before: function(){
                    $(this).parent().find('.csc-current-slide').removeClass('csc-current-slide');
                },
                after: function(){
                    $(this).addClass('csc-current-slide');
                }
            }).hover(function(){
                $(this).cycle('pause');
            }, function(){
                $(this).cycle('resume');
            });
        },

        stop: function(){
            this.$target.find('.csc-slides').cycle('pause');
        }
    });

})();