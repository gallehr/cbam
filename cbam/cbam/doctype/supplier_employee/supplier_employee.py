# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SupplierEmployee(Document):
	def before_save(self):
		if self.is_data_confirmed == True:
			self.status = "Data confirmed by Employee"
		self.confirmed_by_supplier()

	def after_insert(self):
		self.add_child()

	def on_trash(self):
		self.delete_child()
		self.delete_link_in_good()

	def delete_child(self):
		if self.supplier_company:
			supplier_employees = frappe.get_doc("Supplier", self.supplier_company)
			for child in supplier_employees.employees:
				if child.employee_number == self.name: #not tested yet. 
					child.delete()

	def delete_link_in_good(self):
		goods_list = frappe.get_all("Good", filters={"employee": self.name}, fields=["name"])
		for good in goods_list:
			frappe.db.set_value("Good", good, "employee", None)

	def add_child(self):
		supplier_employee = frappe.get_doc("Supplier", self.supplier_company)
		supplier_employee.append("employees", {
			"employee_number": self.name,
			"employee_last_name": self.last_name,
			"employee_email": self.email,
			"is_main_contact": self.is_main_contact
		})
		supplier_employee.save()

	def update_child(self):
		supplier_employees = frappe.get_doc("Supplier", self.supplier_company)
		for child in supplier_employees.employees:
			if child.employee_email == self.email:
				child.employee_number = self.name
				child.employee_last_name = self.last_name
				child.employee_email = self.email
				child.is_main_contact = self.is_main_contact
				supplier_employees.save()

	def confirmed_by_supplier(self):
		user_email = frappe.session.user
		try:
			user = frappe.get_doc("User", user_email)
		except frappe.DoesNotExistError:
			frappe.throw(_("User not found"))
		roles = [role.role for role in user.roles]
		if "Supplier" in roles:
			if self.is_data_confirmed != True:
				frappe.throw("Please check the 'Data Confirmed' checkbox before submitting the form.")