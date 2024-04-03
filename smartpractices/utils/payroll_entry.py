import frappe
from frappe import _
import io

@frappe.whitelist()
def export_sis(payroll_entry):
    payroll_entry_doc = frappe.get_doc('Payroll Entry', payroll_entry)

    if not payroll_entry_doc.docstatus == 1:
        frappe.throw(_("Only submitted documents can be exported"))

    # Write the header
    header = "01"
    header += payroll_entry_doc.name + " " * (25 - len(payroll_entry_doc.name))
    header += "01"
    header += payroll_entry_doc.posting_date.strftime("%d/%m/%Y")
    header += payroll_entry_doc.company + " " * (30 - len(payroll_entry_doc.company))
    company_phone = frappe.get_value("Company", payroll_entry_doc.company, "phone_no")
    if company_phone:
        header += company_phone + " " * (20 - len(company_phone))
    else:
        header += " " * 20

    # Write the header to a text file
    file_name = f'{payroll_entry_doc.name}.txt'
    with io.open(file_name, 'w', encoding='utf-8') as f:
        f.write(header)

    # Attach the file to the Payroll Entry
    with io.open(file_name, 'r', encoding='utf-8') as f:
        file_data = f.read()
    file_doc = frappe.get_doc({
        'doctype': 'File',
        'file_name': file_name,
        'attached_to_doctype': 'Payroll Entry',
        'attached_to_name': payroll_entry,
        'content': file_data,
        'is_private': 1
    })
    file_doc.insert()

    return file_doc.name