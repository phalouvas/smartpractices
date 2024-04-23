import frappe

def before_submit(doc, method):
    # Get quotation items and if the amount is 0 then remove them
    items_to_remove = []
    for item in doc.items:
        if item.amount == 0:
            items_to_remove.append(item)
    for item in items_to_remove:
        doc.items.remove(item)

    # Get the customer of the quotation
    customer = frappe.get_doc("Customer", doc.customer)
    # Get the items of the quotation
    items = doc.items
    # Loop the items and create a new item price for the customer
    for item in items:
        item_price = frappe.db.get_value(
				"Item Price",
				{"item_code": item.item_code, "price_list": "Standard Selling", "customer": customer.name},
				["name", "price_list_rate"],
				as_dict=1,
			)
        if item_price and item_price.price_list_rate != item.rate:
             frappe.db.set_value("Item Price", item_price.name, "price_list_rate", item.rate)
        else:
            if item.rate > 0:
                frappe.get_doc({
                    "doctype": "Item Price",
                    "item_code": item.item_code,
                    "price_list": "Standard Selling",
                    "price_list_rate": item.rate,
                    "customer": customer.name,
                    "uom": item.uom,
                    "selling": 1
                }).insert()