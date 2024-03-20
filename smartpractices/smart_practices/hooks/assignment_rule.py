from collections.abc import Iterable

import frappe
from frappe import _
from frappe.automation.doctype.assignment_rule.assignment_rule import AssignmentRule, get_assignments, reopen_closed_assignment
from frappe.cache_manager import clear_doctype_map, get_doctype_map
from frappe.desk.form import assign_to
from frappe.model import log_types
from frappe.model.document import Document
from frappe.utils.data import comma_and

def apply(doc=None, method=None, doctype=None, name=None):
	doctype = doctype or doc.doctype

	skip_assignment_rules = (
		frappe.flags.in_patch
		or frappe.flags.in_install
		or frappe.flags.in_setup_wizard
		or doctype in log_types
	)

	if skip_assignment_rules:
		return

	if not doc and doctype and name:
		doc = frappe.get_doc(doctype, name)

	assignment_rules = get_doctype_map(
		"Assignment Rule",
		doc.doctype,
		filters={"document_type": doc.doctype, "disabled": 0},
		order_by="priority desc",
	)

	# multiple auto assigns
	assignment_rule_docs: list[AssignmentRule] = [
		frappe.get_cached_doc("Assignment Rule", d.get("name")) for d in assignment_rules
	]

	if not assignment_rule_docs:
		return

	doc = doc.as_dict()
	assignments = get_assignments(doc)

	clear = True  # are all assignments cleared
	new_apply = False  # are new assignments applied

	if assignments:
		# first unassign
		# use case, there are separate groups to be assigned for say L1 and L2,
		# so when the value switches from L1 to L2, L1 team must be unassigned, then L2 can be assigned.
		clear = False
		for assignment_rule in assignment_rule_docs:
			if assignment_rule.is_rule_not_applicable_today():
				continue

			clear = assignment_rule.apply_unassign(doc, assignments)
			if clear:
				break

	# apply rule only if there are no existing assignments
	if clear:
		for assignment_rule in assignment_rule_docs:
			if assignment_rule.is_rule_not_applicable_today():
				continue

			new_apply = assignment_rule.apply_assign(doc)
			if new_apply:
				break

	# apply close rule only if assignments exists
	assignments = get_assignments(doc)

	if assignments:
		for assignment_rule in assignment_rule_docs:
			if assignment_rule.is_rule_not_applicable_today():
				continue

			if not new_apply:
				# only reopen if close condition is not satisfied
				to_close_todos = assignment_rule.safe_eval("close_condition", doc)

				if to_close_todos:
					# close todo status
					todos_to_close = frappe.get_all(
						"ToDo",
						filters={
							"reference_type": doc.doctype,
							"reference_name": doc.name,
						},
						pluck="name",
					)

					for todo in todos_to_close:
						_todo = frappe.get_doc("ToDo", todo)
						_todo.status = "Closed"
						_todo.save(ignore_permissions=True)
					break

				else:
					reopened = reopen_closed_assignment(doc)
					if reopened:
						break

			assignment_rule.close_assignments(doc)
