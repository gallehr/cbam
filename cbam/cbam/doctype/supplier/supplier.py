# The `Supplier` class in the Python code creates a new user in the system based on supplier
# information when the status is "Sent to Supplier".
# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Supplier(Document):
	def after_insert(self):
		self.add_linked_goods_to_childtable()
		if self.status == "Sent to Supplier":
			self.create_new_supplier_user()

	# def before_insert(self):
	# 	add_linked_goods_to_childtable2("SUP-00000003-Liferant3")

	def before_save(self):
		if self.is_data_confirmed == True:
			self.status = "Confirmed by Supplier"

	def create_new_supplier_user(self):
		new_user = frappe.new_doc("User")
		new_user.email = self.company_email
		new_user.first_name = self.supplier_name
		new_user.append("role_profiles", {
			"name": "ibr1s5ocqu",
			"role_profile": "Supplier"
		})
		new_user.insert()

	def add_linked_goods_to_childtable(self):
		good_list = frappe.get_list("Good", pluck="name")
		for good in good_list:
			linked_supplier = frappe.get_value("Good", good, "supplier")
			if linked_supplier == self.name:
				self.append("goods", {
					"good_number": good
				})


# @frappe.whitelist()
# def add_linked_goods_to_childtable2(supplier_name):
# 	supplier = frappe.get_doc("Supplier", supplier_name)
# 	good_list = frappe.get_list("Good", pluck="name")
# 	for good in good_list:
# 		linked_supplier = frappe.get_value("Good", good, "supplier")
# 		# added_goods_list = []
# 		if linked_supplier == supplier.name:
# 			supplier.append("goods", {
# 				"good_number": good
# 			})
# 			# added_goods_list.append(good)
# 			# frappe.msgprint(added_goods_list)
# 	supplier.save()