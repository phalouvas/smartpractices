frappe.ui.form.on('Customer', {
  refresh: function (frm) {
    if (!frm.is_new()) {
      frm.add_custom_button(__('Create Quotation'), function () {
        frappe.confirm(__("Are you sure you want to proceed?"), () => {
          frappe.call({
            method: "smartpractices.utils.customer.create_quotation",
            args: {
              customer: frm.doc.name,
            },
            freeze: true,
            freeze_message: __("Creating Quotation..."),
            callback: function (r) {
              //frappe.ui.toolbar.clear_cache();
              frappe.show_alert({
                message: __("Quotation created"),
                indicator: "green"
              });
              frappe.ui.toolbar.clear_cache();
              frappe.set_route("Form", "Quotation", r.message);
            }
          });
        });
      }, __('Smart Practices'));
    }
  },
});