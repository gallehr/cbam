# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import uuid


class CBAMOperatingCompany(Document):
	def before_insert(self):
		self.add_user_as_contact_person()

	def before_naming(self):
		self.generated_uuid()

	# def on_change(self): # Not working via Web Form
	# 	self.set_full_name()

	def generated_uuid(self):
		generated_uuid = uuid.uuid4()
		self.uuid = generated_uuid

	def add_user_as_contact_person(self):
		if self.select_contact_person == "I am the contact person":
			user_email = frappe.session.user
			try:
				user = frappe.get_doc("User", user_email)
			except frappe.DoesNotExistError:
				frappe.throw(_("User not found"))
			role_list = [r.role for r in user.roles]
			if "Supplier" in role_list:
				employee_list = frappe.get_all("Supplier Employee", filters={"email": user_email}, fields=["name"], pluck="name")
				if not employee_list:
					frappe.throw("You are not registered as an employee of a supplier. Please register first.")
				elif len(employee_list) > 1:
					frappe.throw("You are registered as an employee of more than one supplier. Please contact the system administrator.")
				else:
					self.contact_person_employee = employee_list[0]

	def set_full_name(self): # Not working via Web Form
		has_first_name_changed = self.has_value_changed("first_name")
		has_last_name_changed = self.has_value_changed("last_name")
		if has_first_name_changed or has_last_name_changed:
			self.full_name = self.first_name + " " + self.last_name