# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Good(Document):
	def validate(self):
		self.get_responsible_employee()

	def get_responsible_employee(self):
		if self.supplier and not self.employee:
			supplier_doc = frappe.get_doc("Supplier", self.supplier)
			for child in supplier_doc.employees:
				if child.is_main_contact == True:
					main_contact = child.employee_email
					self.employee = main_contact

