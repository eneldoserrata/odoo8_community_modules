    openerp.bista_advance_nav = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt,
        QWeb = instance.web.qweb;

    instance.web.Menu.include({

        bind_menu: function() {
            var self = this;
            if($('nav ul li.tnav ul').closest("li").children("ul").length) {
               $('nav ul li.tnav ul').closest("li").children("ul li a").append('<b class="caret"></b>');
            }
            this.$secondary_menus = this.$el.parents().find('.oe_secondary_menus_container')
            this.$secondary_menus.on('click', 'a[data-menu]', this.on_menu_click);
            this.$el.on('click', 'a[data-menu]', this.on_top_menu_click);
            // Hide second level submenus
            this.$secondary_menus.find('.oe_menu_toggler').siblings('.oe_secondary_submenu').hide();
            if (self.current_menu) {
                self.open_menu(self.current_menu);
            }
            this.trigger('menu_bound');

            var lazyreflow = _.debounce(this.reflow.bind(this), 200);
            instance.web.bus.on('resize', this, function() {
                if (parseInt(self.$el.parent().css('width')) <= 768 ) {
                    lazyreflow('all_outside');
                } else {
                    lazyreflow();
                }
            });
            instance.web.bus.trigger('resize');
            $('nav#oe_main_menu_navbar ul li ul.oe_secondary_submenu').addClass("tnav");
            $('.oe_leftbar_open').toggle(
                function(){
                    $(this).removeClass("show1");
                    $(".oe_leftbar").fadeIn(500).removeClass("leftbarhide")},
                function(){
                    $(this).addClass("show1");
                    $(".oe_leftbar").fadeOut(500).addClass("leftbarhide");
                   });
            this.is_bound.resolve();
        },
        reflow: function(behavior) {
            var self = this;
            var $more_container = this.$('#menu_more_container').hide();
            var $more = this.$('#menu_more');
            var $systray = this.$el.parents().find('.oe_systray');
            $more.children('li').insertBefore($more_container);  // Pull all the items out of the more menu
            // 'all_outside' beahavior should display all the items, so hide the more menu and exit
            if (behavior === 'all_outside') {
                this.$el.find('li').show();
                $more_container.hide();
                return;
            }
            var $toplevel_items = this.$el.find('li.tnav').not($more_container).not($systray.find('li')).hide();
            $toplevel_items.each(function() {
                // In all inside mode, we do not compute to know if we must hide the items, we hide them all
                if (behavior === 'all_inside') {
                    return false;
                }
                var remaining_space = self.$el.parent().width() - $more_container.outerWidth();
                self.$el.parent().children(':visible').each(function() {
                    remaining_space -= $(this).outerWidth() + 55;
                });
                if ($(this).width() > remaining_space) {
                    return false;
                }
                $(this).show();
            });
            $more.append($toplevel_items.filter(':hidden').show());
            $more_container.toggle(!!$more.children().length || behavior === 'all_inside');
            // Hide toplevel item if there is only one
            var $toplevel = this.$el.children("li.tnav:visible");
            if ($toplevel.length === 1 && behavior != 'all_inside') {
                $toplevel.hide();
            }
        },
    });
    };
