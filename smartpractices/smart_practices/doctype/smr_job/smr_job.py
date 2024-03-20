# Copyright (c) 2024, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.cache_manager import get_doctype_map
from frappe.model.document import Document

class SmrJob(Document):
	pass

@frappe.whitelist()
def create_jobs(customer):
	job_groups = get_doctype_map(
		"Smr Job Group",
		"Smr Job Non Groups",
		filters={"is_group": 0}
	)
	existing_jobs = get_doctype_map(
		"Smr Job",
		"Smr Job Non Groups",
		filters={"customer": customer}
	)