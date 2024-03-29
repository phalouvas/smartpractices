frappe.ui.form.on('Customer', {
    refresh: function (frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Jobs'), function () {
                frappe.confirm(__("Are you sure you want to proceed?"), () => {
                    frappe.call({
                      method: "smartpractices.smart_practices.doctype.smr_job.smr_job.create_jobs",
                      args: {
						customer: frm.doc.name,
					},
                      freeze: true,
                      freeze_message: __("Creating Jobs Data..."),
                      callback: function(r) {
                        //frappe.ui.toolbar.clear_cache();
                        frappe.show_alert({
                          message: __("Jobs created"),
                          indicator: "green"
                        });
                      }
                    });
                  });
            }).addClass('btn-primary');
        }
    },
});