import frappe

def before_submit(doc, method):
    # Get quotation items and if the amount is 0 then remove them
    items_to_remove = []
    for item in doc.items:
        if item.amount == 0:
            items_to_remove.append(item)
    for item in items_to_remove:
        doc.items.remove(item)