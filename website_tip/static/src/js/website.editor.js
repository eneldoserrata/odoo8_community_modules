$(document).ready(function() {
    'use strict';

    var website = openerp.website;
    website.add_template_file('/website_tip/static/src/xml/website.editor.xml');

    website.editor.RTELinkDialog = website.editor.RTELinkDialog.extend({
        tip_text: false,
        tip_position: false,
        tip_background: false,
        tip_color: false,
        events: _.extend({}, website.editor.RTELinkDialog.prototype.events, {
            'change input#link-tip-text': function(e) {
                this.tip_text = $(e.target).val();
                this.preview_tip();
            },
            'change input[name="link-tip-position"]': function(e) {
                this.tip_position = $(e.target).val();
                this.preview_tip();
            },
            'change input#link-tip-background': function(e) {
                this.tip_background = $(e.target).val();
                this.preview_tip();
            },
            'change input#link-tip-color': function(e) {
                this.tip_color = $(e.target).val();
                this.preview_tip();
            },
            'change select#link-tip-animation-in': function(e) {
                this.tip_animation_in = $(e.target).val();
                this.preview_tip();
            },
            'change select#link-tip-animation-out': function(e) {
                this.tip_animation_out = $(e.target).val();
                this.preview_tip();
            },
            'change input#link-tip-onload': function(e) {
                this.tip_onload = $(e.target).is(':checked') ? true : false;
                this.preview_tip();
            }
        }),
        preview_tip: function() {
            var preview = this.$("#link-preview");
            preview.attr({
                'data-tipso': this.tip_text || '',
                'data-tipso-position': this.tip_position || '',
                'data-tipso-background': this.tip_background || '',
                'data-tipso-color': this.tip_color || '',
                'data-tipso-animationin': this.tip_animation_in || 'fadeIn',
                'data-tipso-animationout': this.tip_animation_out || 'fadeOut',
                'data-tipso-onload': this.tip_onload || ''
            })
            hook_tipso(preview);
        },
        bind_data: function() {
            var self = this;
            this._super();
            var tip_text = this.element ? this.element.getAttribute('data-tipso') : '';
            var tip_position = this.element ? this.element.getAttribute('data-tipso-position') : '';
            var tip_background = this.element ? this.element.getAttribute('data-tipso-background') : '';
            var tip_color = this.element ? this.element.getAttribute('data-tipso-color') : '';
            var tip_animation_in = this.element ? this.element.getAttribute('data-tipso-animationin') : 'fadeIn';
            var tip_animation_out = this.element ? this.element.getAttribute('data-tipso-animationout') : 'fadeOut';
            this.$('input#link-tip-text').val(tip_text).trigger('change');
            this.$('input[name="link-tip-position"][value="' + tip_position + '"]').prop('checked', true).trigger('change');
            this.$('input#link-tip-background').val(tip_background).trigger('change').colorpicker().on('changeColor.colorpicker', function(event) {
                $(this).trigger('change');
            });
            this.$('input#link-tip-color').val(tip_color).trigger('change').colorpicker().on('changeColor.colorpicker', function(event) {
                $(this).trigger('change');
            });
            this.$('select#link-tip-animation-in').val(tip_animation_in).trigger('change');
            this.$('select#link-tip-animation-out').val(tip_animation_out).trigger('change');
            this.$('input#link-tip-onload').prop('checked', this.tip_onload).trigger('change');
        },
        save: function() {
            var self = this;
            this._super();

            if (!this.element) {
                var element;
                if ((element = this.get_selected_link()) && element.hasAttribute('href')) {
                    this.editor.getSelection().selectElement(element);
                }
                this.element = element;
            }
            if (this.element) {
                this.element.setAttributes({
                    'data-tipso': this.tip_text || '',
                    'data-tipso-position': this.tip_position || '',
                    'data-tipso-background': this.tip_background || '',
                    'data-tipso-color': this.tip_color || '',
                    'data-tipso-animationin': this.tip_animation_in || 'fadeIn',
                    'data-tipso-animationout': this.tip_animation_out || 'fadeOut',
                    'data-tipso-onload': this.tip_onload || ''
                });
            }
        }
    });
});