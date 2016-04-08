openerp.ir_export_extended_ept = function(instance) {
	instance.web.DataExport.include({	
		
	    do_save_export_list: function(value) {
	        var self = this;
	        var fields = self.get_fields();
	        if (!fields.length) {
	            return;
	        }
	        var seq = 0;
	        this.exports.create({
	            name: value,
	            resource: this.dataset.model,
	            domain: this.domain,
	            export_fields: _(fields).map(function (field) {
	            	seq++;
	            	var v = field['f_t'] ;
	                return [0, 0, {sequence:seq,name: field['f_v'],heading:v}];
	            })
	        }).then(function (export_list_id) {
	            if (!export_list_id) {
	                return;
	            }
	            if (!self.$el.find("#saved_export_list").length || self.$el.find("#saved_export_list").is(":hidden")) {
	                self.show_exports_list();
	            }
	            self.$el.find("#saved_export_list").append( new Option(value, export_list_id) );
	        });
	        this.on_show_save_list();
	    },

	    get_fields: function() {
	        var export_fields = this.$("#fields_list option").map(function() {
	            var val_ept = {'f_v':$(this).val(),'f_t':$(this).text()}
	        	return val_ept;
	        }).get();
	        if (!export_fields.length) {
	            alert(_t("Please select fields to save export list..."));
	        }
	        return export_fields;
	    },
	    
	});
};