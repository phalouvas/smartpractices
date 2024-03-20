import frappe
from frappe.core.doctype.data_import.data_import import import_file
import os
import frappe
from frappe.core.doctype.data_import.data_import import import_file

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
