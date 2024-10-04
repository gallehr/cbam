# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CBAMEmissionData(Document):
	def after_insert(self):
		self.add_to_installation_cht()

	def on_trash(self):
		self.delete_child_from_installation_cht()


	def add_to_installation_cht(self):
		has_installation_name_changed = self.has_value_changed("installation_name")
		if has_installation_name_changed:
			installation = frappe.get_doc("CBAM Installation", self.installation_name)
			installation.append("emission_datas", {
				"emission_data": self.name,
			})
			installation.save()

	def delete_child_from_installation_cht(self):
		if self.installation_name:
			installation = frappe.get_doc("CBAM Installation", self.installation_name)
			for child in installation.emission_datas:
				if child.emission_data == self.name:
					child.delete()
