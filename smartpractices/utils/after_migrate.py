import frappe

def customer_links():
	# Check "DocType Link" if there is entry for link_doctype with value "Register Company"
	if not frappe.db.exists("DocType Link", {"link_doctype": "Register Company", "parent": "Company"}):
		# Create a new entry in "DocType Link" with link_doctype "Register Company"
		frappe.get_doc({
			"doctype": "DocType Link",
			"link_doctype": "Register Company",
			"link_fieldname": "company",
			"parenttype": "Customize Form",
			"parent": "Company",
			"parentfield": "links",
			"group": "Orders",
			"custom": 1
		}).insert()