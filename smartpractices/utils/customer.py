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