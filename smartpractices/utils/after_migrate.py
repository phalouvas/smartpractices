import frappe
from frappe.core.doctype.data_import.data_import import import_file
import os
from frappe.permissions import add_permission, update_permission_property

def import_job_groups():
    # Check if Smr Job Group already has data
    if frappe.get_all("Smr Job Group"):
        return

    # Get the directory path of the current file
    file_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(file_dir, 'Smr Job Group 1.csv')
    import_file("Smr Job Group", file_path, "Insert", False, True)

    file_path = os.path.join(file_dir, 'Smr Job Group 2.csv')
    import_file("Smr Job Group", file_path, "Insert", False, True)

def give_read_access():
    add_permission("Smr Job Group", "Sales User", 0)
    update_permission_property("Smr Job Group", "Sales User", 0, "read", 1)
    add_permission("Smr Job Group", "Sales Manager", 0)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "read", 1)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "write", 1)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "create", 1)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "delete", 1)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "share", 1)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "report", 1)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "print", 1)
    update_permission_property("Smr Job Group", "Sales Manager", 0, "email", 1)

    add_permission("Smr Job", "Sales User", 0)
    update_permission_property("Smr Job", "Sales User", 0, "read", 1)
    add_permission("Smr Job", "Sales Manager", 0)
    update_permission_property("Smr Job", "Sales Manager", 0, "read", 1)
    update_permission_property("Smr Job", "Sales Manager", 0, "write", 1)
    update_permission_property("Smr Job", "Sales Manager", 0, "create", 1)
    update_permission_property("Smr Job", "Sales Manager", 0, "delete", 1)
    update_permission_property("Smr Job", "Sales Manager", 0, "share", 1)
    update_permission_property("Smr Job", "Sales Manager", 0, "report", 1)
    update_permission_property("Smr Job", "Sales Manager", 0, "print", 1)
    update_permission_property("Smr Job", "Sales Manager", 0, "email", 1)
