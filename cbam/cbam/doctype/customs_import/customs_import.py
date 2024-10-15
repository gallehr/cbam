# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomsImport(Document):
	def on_trash(self):
		self.delete_all_goods()

	def delete_all_goods(self):
		for good in self.goods:
			frappe.db.set_value("Good", good.name, "internal_customs_import_number", None)
			frappe.db.delete("Good", {
				"name": good.name
			})