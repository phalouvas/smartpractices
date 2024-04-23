import frappe

def customer_links():
	# Check "DocType Link" if there is entry for link_doctype with value "Register Company"
	if not frappe.db.exists("DocType Link", {"link_doctype": "Register Company", "parent": "Customer"}):
		# Create a new entry in "DocType Link" with link_doctype "Register Company"
		frappe.get_doc({
			"doctype": "DocType Link",
			"link_doctype": "Register Company",
			"link_fieldname": "customer",  # Assuming "Register Company" DocType has a link field to "Customer"
			"parenttype": "Customize Form",
			"parent": "Customer",
			"parentfield": "links",
			"group": "Orders",
			"custom": 1
		}).insert()