import frappe

def give_read_access():
    # Give read access to "Sales User" on "Smr Job Groups"
    frappe.permissions.add_permission("Smr Job Groups", "Sales User", read=1)

    # Give read access to "Sales User" on "Smr Job"
    frappe.permissions.add_permission("Smr Job", "Sales User", read=1)
