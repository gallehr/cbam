# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import uuid


class CBAMOperatingCompany(Document):
	def before_naming(self):
		self.generated_uuid()

	def validate(self):
		self.add_user_as_contact_person()
		self.set_full_name()
		self.set_parent_supplier()

	def generated_uuid(self):
		generated_uuid = uuid.uuid4()
		self.uuid = generated_uuid

	def check_if_user_supplieruser(self):
		user_email = frappe.session.user
		try:
			user = frappe.get_doc("User", user_email)
		except frappe.DoesNotExistError:
			frappe.throw(_("User not found"))
		role_list = [r.role for r in user.roles]
		if "Supplier" in role_list:
			employee_list = frappe.get_all("Supplier Employee", filters={"email": user_email}, fields=["name"], pluck="name")
			if not employee_list:
				frappe.throw("You are not registered as an employee of a supplier. Please login with another user.")
				return False
			elif len(employee_list) > 1:
				frappe.throw("You are registered as an employee of more than one supplier. Please contact the system administrator.")
				return False
			else:
				return True, employee_list
		else:
			frappe.throw("You are not registered as a supplier. Please choose 'Different contact person' and add the contact person manually.")

	def add_user_as_contact_person(self):
		has_select_contact_person_changed = self.has_value_changed("select_contact_person")
		if has_select_contact_person_changed:
			is_user_supplier, employee_list = self.check_if_user_supplieruser()
			if self.select_contact_person == "I am the contact person" and is_user_supplier:
				self.contact_person_employee = employee_list[0]
				supplier_employee = frappe.get_doc("Supplier Employee", employee_list[0])
				self.first_name = supplier_employee.first_name
				self.last_name = supplier_employee.last_name
				self.email = supplier_employee.email
				self.phone_number = supplier_employee.phone_number
				self.position_in_the_company = supplier_employee.position

	def set_full_name(self):
		if self.first_name and self.last_name:
			self.full_name = self.first_name + " " + self.last_name

	def set_parent_supplier(self):
		is_user_supplier, employee_list = self.check_if_user_supplieruser()
		if is_user_supplier:
			try:
				supplier = frappe.db.get_value("Supplier Employee", employee_list[0], "supplier_company")
				self.parent_supplier = supplier
			except frappe.DoesNotExistError:
				frappe.throw("Supplier not found")
