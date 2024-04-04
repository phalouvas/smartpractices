import frappe
from frappe import _
import io

@frappe.whitelist()
def export_sis(payroll_entry):
    payroll_entry_doc = frappe.get_doc('Payroll Entry', payroll_entry)

    if not payroll_entry_doc.docstatus == 1:
        frappe.throw(_("Only submitted documents can be exported"))

    lines = ""

    lines += get_header_record(payroll_entry_doc)
    lines += get_schedule_details(payroll_entry_doc)
    # get all submitted Salary Slip of the Payroll Entry
    salary_slips = frappe.get_all('Salary Slip', filters={'payroll_entry': payroll_entry, 'docstatus': 1}, fields=['name', 'employee', 'rounded_total'])
    for salary_slip in salary_slips:
        lines += get_employees_earnings(salary_slip)
    lines += get_schedule_totals(payroll_entry_doc)

    # Write the line to a text file
    file_name = f'{payroll_entry_doc.name}.txt'
    with io.open(file_name, 'w', encoding='utf-8') as f:
        f.write(lines)

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

    return "Social Insurance file created succesfully!"

def get_header_record(payroll_entry_doc):
    """
    Generate the header record for the payroll entry.

    Args:
        payroll_entry_doc (object): The payroll entry document.

    Returns:
        str: The generated header record.
    """
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

    line += '\n'
    return line

def get_schedule_details(payroll_entry_doc):
    """
    Get the schedule details for a payroll entry.

    Args:
        payroll_entry_doc (object): The payroll entry document.

    Returns:
        str: The schedule details line.

    Raises:
        frappe.ValidationError: If the Social Insurance Number or Employees Category or Earnings Type is not set.
    """
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

    start_date = payroll_entry_doc.start_date.strftime("%m/%Y")

    line += start_date
    line += " " * 14

    line += '\n'
    return line

def get_employees_earnings(salary_slip):    
    employee = frappe.get_doc('Employee', salary_slip.employee)
    
    # Input Code
    line = "04"
    
    # Social Insurance Number
    if employee.custom_sis_no:
        line += "0" * (8 - len(employee.custom_sis_no)) + employee.custom_sis_no
    else:
        line += "0" * 8

    # Identity Card Number
    if employee.custom_identity_card_no:
        line += "0" * (8 - len(employee.custom_identity_card_no)) + employee.custom_identity_card_no
    else:
        line += "0" * 8

    # Aliens Registration Number
    if employee.custom_aliens_registration_no:
        line += "0" * (8 - len(employee.custom_aliens_registration_no)) + employee.custom_aliens_registration_no
    else:
        line += "0" * 8

    # Actual Earnings
    line += 'S' + str(int(salary_slip.rounded_total)).replace('.', '').rjust(10, '0')

    # General Health System Earnings
    line += 'S' + str(int(salary_slip.rounded_total)).replace('.', '').rjust(10, '0')

    # Insurable Earnings
    line += 'S' + str(int(salary_slip.rounded_total)).replace('.', '').rjust(10, '0')

    # Contributions to the Central Holiday Fund 
    line += 'S' + "0" * 12

    line += "0" * 15
    line += '1\n'

    return line

def get_schedule_totals(payroll_entry_doc):
    """
    Get the schedule totals for a payroll entry.

    Args:
        payroll_entry_doc (object): The payroll entry document.

    Returns:
        str: The schedule totals line.
    """
    line = "05"
    salary_slips = frappe.get_all('Salary Slip', filters={'payroll_entry': payroll_entry_doc.name, 'docstatus': 1}, fields=['rounded_total'])
    total_rounded_total = sum([float(salary_slip['rounded_total']) for salary_slip in salary_slips])
    
    # Actual Earnings Total 
    line += 'S' + str(int(total_rounded_total)).replace('.', '').rjust(12, '0')

    # General Health System Earnings Total
    line += 'S' + str(int(total_rounded_total)).replace('.', '').rjust(12, '0')

    # Insurable Earnings Total
    line += 'S' + str(int(total_rounded_total)).replace('.', '').rjust(12, '0')

    # Contributions to the Central Holiday Fund
    line += 'S' + "0" * 14

    # Number of New Employees
    line += "0" * 5

    # Number of Employees whose employment has been terminated
    line += "0" * 5

    # Total number of Employees
    line += str(len(salary_slips)).rjust(6, '0')

    return line