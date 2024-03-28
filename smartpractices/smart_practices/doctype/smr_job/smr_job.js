frappe.ui.form.on('Smr Job', {
    onload: function(frm) {
        frappe.call({
            method: 'smartpractices.smart_practices.doctype.smr_job.smr_job.get_items',
            callback: function(response) {
                frm.set_query('item', function() {
                    return {
                        filters: {
                            'name': ['in', response.message.map(item => item.name)]
                        }
                    };
                });
            }
        });
    }
});