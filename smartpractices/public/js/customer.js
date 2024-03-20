frappe.ui.form.on('Customer', {
    refresh: function (frm) {

        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Jobs'), function () {
                frappe.model.open_mapped_doc({
                    method: "smartpractices.smart_practices.doctype.smr_job.smr_job.create_jobs",
                    frm: frm
                });
            }).addClass('btn-primary');
        }
    },
});
