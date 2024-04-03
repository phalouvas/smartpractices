import frappe
from frappe.core.doctype.data_import.data_import import import_file
import os
from frappe.permissions import add_permission, update_permission_property

def import_item_groups():
	file_dir = os.path.dirname(os.path.abspath(__file__))
	file_path = os.path.join(file_dir, 'Salary Component.csv')
	import_file("Salary Component", file_path, "Insert", False, True)
	import_social_insurance()
	# Check if Item Group "Smart Practices" exists. If exists return else create it
	if frappe.db.exists("Item Group", "Smart Practices"):
		return
	
	import_app_data()
	create_project_template()	

def import_app_data():
	item_group = frappe.get_doc({
		"doctype": "Item Group",
		"item_group_name": "Smart Practices",
		"parent_item_group": "All Item Groups",
		"is_group": 1
	})
	
	item_group.insert(ignore_permissions=True)
	frappe.db.commit()

	# Get the directory path of the current file
	file_dir = os.path.dirname(os.path.abspath(__file__))

	file_path = os.path.join(file_dir, 'Item Group.csv')
	import_file("Item Group", file_path, "Insert", False, True)

	file_path = os.path.join(file_dir, 'Item.csv')
	import_file("Item", file_path, "Insert", False, True)

	file_path = os.path.join(file_dir, 'Task Type.csv')
	import_file("Task Type", file_path, "Insert", False, True)

	file_path = os.path.join(file_dir, 'Task.csv')
	import_file("Task", file_path, "Insert", False, True)

	file_path = os.path.join(file_dir, 'Module Profile.csv')
	import_file("Module Profile", file_path, "Insert", False, True)

	file_path = os.path.join(file_dir, 'Role Profile.csv')
	import_file("Role Profile", file_path, "Insert", False, True)
	 
	file_path = os.path.join(file_dir, 'Salary Component.csv')
	import_file("Salary Component", file_path, "Insert", False, True)
	import_social_insurance()
	 
def create_project_template():
	if frappe.db.exists("Project Template", "Smart Practices"):
		return
	
	# Get all tasks that have status as "Teplate" and Task Type one of "Audit and assurances", "Corporate", "Taxation", "Accounting"
	tasks = frappe.get_all("Task", filters={"status": "Template", "type": ["in", ["Audit and assurances", "Corporate", "Taxation", "Accounting"]]}, fields=["name"])

	project_template = frappe.get_doc({
		"doctype": "Project Template",
		"name": "Smart Practices",
		"project_type": "Internal",
		"is_active": 1,
		"default": 1
	})

	for task in tasks:
		project_template.append("tasks", {
			"task": task.name
		})
	
	project_template.insert(ignore_permissions=True)
	frappe.db.commit()

def import_social_insurance():
	# Get account with account_name "Salary"
	salary_account = frappe.get_doc("Account", {"account_name": "Salary"})
	# If account does not exist, return
	if not salary_account:
		return
	
	# Get salary component with component_name "Basic"
	salary_component = frappe.get_doc("Salary Component", "Basic")
	salary_component.is_tax_applicable = 0
	salary_component.depends_on_payment_days = 0
	salary_component.amount_based_on_formula = 1
	salary_component.formula = "base * 1"
	salary_component.save(ignore_permissions=True)

	# Loop through all existing salary components and update the account to "Salary"
	salary_components = frappe.get_all("Salary Component", filters={"account": ""}, fields=["name","amount_based_on_formula","formula"])
	for salary_component in salary_components:
		salary_component_doc = frappe.get_doc("Salary Component", salary_component.name)
		salary_component_doc.append("accounts", {"account": salary_account.name})
		salary_component_doc.save(ignore_permissions=True)

	frappe.db.commit()

	# Create a new salary structure "Smart Practices" and add all salary components to it
	salary_structure = frappe.get_doc({
		"doctype": "Salary Structure",
		"name": "Smart Practices",
		"is_active": "Yes",
	})
	for salary_component in salary_components:
		salary_structure.append("earnings", {
			"salary_component": salary_component.name,
			"amount_based_on_formula": salary_component.amount_based_on_formula,
			"formula": salary_component.formula,
			})
	
	salary_structure.insert(ignore_permissions=True)
	salary_structure.submit()
	