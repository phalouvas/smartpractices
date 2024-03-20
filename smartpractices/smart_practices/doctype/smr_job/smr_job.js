frappe.ui.form.on('Smr Job', {
    onload: function(frm) {
        frm.set_query('job_group', function() {
            return {
                filters: {
                    'is_group': 0
                }
            };
        });
    }
});