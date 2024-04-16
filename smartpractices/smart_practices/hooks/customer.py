import frappe

from erpnext.crm.doctype.lead.lead import Lead as OriginalLead

def after_insert(doc, method):
    customer_information = frappe.new_doc("Customer Information")
    customer_information.customer = doc.name
    customer_information.insert(ignore_permissions=True)
    doc.db_set('custom_customer_information', customer_information.name)

    doc.reload()

# Hook: before delete
def after_delete(doc, method):
    # if custom_customer_information is not empty
    if doc.get('custom_customer_information'):
        # delete the customer consent document
        frappe.delete_doc("Customer Information", doc.get('custom_customer_information'))
