# Copyright (c) 2024, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.cache_manager import get_doctype_map
from frappe.model.document import Document

class SmrJob(Document):
	pass

@frappe.whitelist()
def create_jobs(customer):
	job_groups = frappe.get_all("Smr Job Group", filters={"is_group": 0})
	existing_jobs = frappe.get_all("Smr Job", filters={"customer": customer, "disabled": 0})
	for job in existing_jobs:
		job_doc = frappe.get_doc("Smr Job", job.name)
		job_doc.disabled = 1
		job_doc.save()
		job_doc.delete()

	return job_groups