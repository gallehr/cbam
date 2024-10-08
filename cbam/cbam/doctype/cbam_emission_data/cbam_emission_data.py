# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CBAMEmissionData(Document):
	def after_insert(self):
		self.add_to_installation_cht()

	def on_trash(self):
		self.delete_child_from_installation_cht()
		self.delete_link_in_good()


	def add_to_installation_cht(self):
		has_cbam_installation_changed = self.has_value_changed("cbam_installation")
		if has_cbam_installation_changed:
			installation = frappe.get_doc("CBAM Installation", self.cbam_installation)
			installation.append("emission_datas", {
				"emission_data": self.name,
			})
			installation.save()

	def delete_child_from_installation_cht(self):
		if self.cbam_installation:
			installation = frappe.get_doc("CBAM Installation", self.cbam_installation)
			for child in installation.emission_datas:
				if child.emission_data == self.name:
					child.delete()

	def delete_link_in_good(self):
		linked_goods_list = frappe.get_all("Good", filters={"emission_data": self.name}, fields=["name"], pluck="name")
		for good in linked_goods_list:
			frappe.db.set_value("Good", good, "emission_data", None)
