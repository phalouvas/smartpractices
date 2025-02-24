// Copyright (c) 2024, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on("Related Person", {
    refresh(frm) {
        if (frm.doc.__islocal) {
			hide_field(["address_html", "contact_html", "address_contacts"]);
			frappe.contacts.clear_address_and_contact(frm);
		} else {
			unhide_field(["address_html", "contact_html", "address_contacts"]);
			frappe.contacts.render_address_and_contact(frm);
		}
    },
});
