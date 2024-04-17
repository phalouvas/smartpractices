import frappe

def after_insert(doc, method):
    # Return if empty sales order
    if not doc.sales_order:
        return
    
    # Get the sales order items
    sales_order_items = frappe.get_all("Sales Order Item", filters={"parent": doc.sales_order}, fields=["item_code", "description"])
    
    # Create project tasks. Assign on the item_code to subject and description to description
    for item in sales_order_items:
        frappe.get_doc({
            "doctype": "Task",
            "subject": item.item_code,
            "description": item.description,
            "project": doc.name
        }).insert()
    