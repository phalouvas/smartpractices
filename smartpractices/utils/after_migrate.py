import frappe
from frappe.core.doctype.data_import.data_import import import_file
import os
from frappe.permissions import add_permission, update_permission_property

def import_item_groups():
    # Check if Item Group "Smart Practices" exists. If exists return else create it
    if frappe.db.exists("Item Group", "Smart Practices"):
        return

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