import frappe
from frappe import _
import io

@frappe.whitelist()
def export_sis(payroll_entry):
    payroll_entry_doc = frappe.get_doc('Payroll Entry', payroll_entry)

    if not payroll_entry_doc.docstatus == 1:
        frappe.throw(_("Only submitted documents can be exported"))

    # Header record
    line = "01"
    line += payroll_entry_doc.name + " " * (25 - len(payroll_entry_doc.name))
    line += "01"
    line += payroll_entry_doc.posting_date.strftime("%d/%m/%Y")
    line += payroll_entry_doc.company + " " * (30 - len(payroll_entry_doc.company))
    company_phone = frappe.get_value("Company", payroll_entry_doc.company, "phone_no")
    if company_phone:
        line += company_phone + " " * (20 - len(company_phone))
    else:
        line += " " * 20

    # Write the line to a text file
    file_name = f'{payroll_entry_doc.name}.txt'
    with io.open(file_name, 'w', encoding='utf-8') as f:
        f.write(line + '\n')

    # Schedule Details
    line = "02"
    custom_sis_number = payroll_entry_doc.custom_sis_number
    if custom_sis_number:
        # Verify that the custom_sis_number is 15 characters long and in format 99999999/9/9999
        if len(custom_sis_number) != 15:
            frappe.throw(_("The Social Insurance Number in the Company master must be 15 characters long"))
        if custom_sis_number[8] != '/':
            frappe.throw(_("The Social Insurance Number in the Company master must be in the format 99999999/9/9999"))
        line += custom_sis_number + " " * (15 - len(custom_sis_number))
    else:
        frappe.throw(_("Please set the Social Insurance Number"))

    # get company custom_employers_type
    custom_employees_category = payroll_entry_doc.custom_employees_category
    if custom_employees_category:
        line += custom_employees_category
    else:
        frappe.throw(_("Please set the Employees Category"))

    custom_earnings_type = payroll_entry_doc.custom_earnings_type
    if custom_earnings_type:
        line += custom_earnings_type
    else:
        frappe.throw(_("Please set the Earnings Type"))

    # Delete existing file with the same name
    existing_file = frappe.get_value('File', {'file_name': file_name})
    if existing_file:
        frappe.delete_doc('File', existing_file)

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