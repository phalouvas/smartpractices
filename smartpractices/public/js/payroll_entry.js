frappe.ui.form.on('Payroll Entry', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {  // Check if the Payroll Entry is submitted
            frm.add_custom_button(__('SIS Export'), function() {
                frappe.call({
                    method: 'smartpractices.utils.payroll_entry.export_sis',
                    args: {
                        payroll_entry: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: __("Exporting Payroll Entry..."),
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(r.message);
                        }
                        frm.reload_doc();
                    }
                });
            });
        }
    }
});