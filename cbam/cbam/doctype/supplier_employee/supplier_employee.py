# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SupplierEmployee(Document):
	def before_save(self):
		if self.is_data_confirmed == True:
			self.status = "Confirmed by Supplier"
