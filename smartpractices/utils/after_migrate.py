import frappe

def import_item_groups():
	# Check if Item Group "Smart Practices" exists. If exists return else create it
	if frappe.db.exists("Item Group", "Smart Practices"):
		return
	
	pass