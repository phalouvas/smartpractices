import frappe

def get_items():
	return frappe.db.sql("""
		SELECT name FROM `tabItem`
		WHERE item_group IN (
			SELECT name FROM `tabItem Group`
			WHERE lft >= (SELECT lft FROM `tabItem Group` WHERE name = 'Smart Practices')
			AND rgt <= (SELECT rgt FROM `tabItem Group` WHERE name = 'Smart Practices')
		)
	""", as_dict=1)

@frappe.whitelist()
def create_quotation(customer):

    items = get_items()
    quotation = frappe.new_doc("Quotation")
    quotation.customer = customer
    quotation.items = []
    for item in items:
        quotation.append("items", {
            "item_code": item.name,
            "qty": 1
        })
    quotation.insert()
    quotation.submit()
    return quotation.name

@frappe.whitelist()
def create_sales_order(customer):

    items = get_items()
    sales_order = frappe.new_doc("Sales Order")
    sales_order.customer = customer
    # set delivery_date as 7 days from today
    sales_order.delivery_date = frappe.utils.add_days(frappe.utils.nowdate(), 7)
    sales_order.items = []
    for item in items:
        sales_order.append("items", {
            "item_code": item.name,
            "qty": 1
        })
    sales_order.insert()
    sales_order.submit()
    return sales_order.name