# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SupplierEmployee(Document):
	def before_save(self):
		if self.is_data_confirmed == True:
			self.status = "Data confirmed by Employee"

	def on_trash(self):
		self.delete_child()

	def delete_child(self):
		supplier_employees = frappe.get_doc("Supplier", self.supplier_company)
		for child in supplier_employees.employees:
			if child.employee_email == self.email:
				child.delete()