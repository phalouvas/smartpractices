import frappe
from frappe.permissions import add_permission

def after_install():
    add_standard_navbar_items()

def add_standard_navbar_items():
	navbar_settings = frappe.get_single("Navbar Settings")

	erpnext_navbar_items = [
		{
			"item_label": "About Smart Practices",
			"item_type": "Route",
			"route": "https://kainotomo.com/",
			"is_standard": 0,
		},		
	]

	current_navbar_items = navbar_settings.help_dropdown
	navbar_settings.set("help_dropdown", [])

	for item in erpnext_navbar_items:
		current_labels = [item.get("item_label") for item in current_navbar_items]
		if not item.get("item_label") in current_labels:
			navbar_settings.append("help_dropdown", item)

	for item in current_navbar_items:
		navbar_settings.append(
			"help_dropdown",
			{
				"item_label": item.item_label,
				"item_type": item.item_type,
				"route": item.route,
				"action": item.action,
				"is_standard": item.is_standard,
				"hidden": item.hidden,
			},
		)

	navbar_settings.save()


def fix_permissions():
	# Set permissions for Role "Project Manager" to access "Project Template"
	add_permission("Role", "Project Manager", "Project Template")
	