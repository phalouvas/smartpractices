# Copyright (c) 2024, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe.defaults
from frappe import _, msgprint, qb
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from frappe.model.mapper import get_mapped_doc
from frappe.model.naming import set_name_by_naming_series, set_name_from_naming_options
from frappe.model.utils.rename_doc import update_linked_doctypes
from frappe.utils import cint, cstr, flt, get_formatted_email, today
from frappe.utils.deprecations import deprecated
from frappe.utils.user import get_users_with_role

class RelatedPerson(Document):
	
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
