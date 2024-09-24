# The `Supplier` class in the Python code creates a new user in the system based on supplier
# information when the status is "Sent to Supplier".
# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Supplier(Document):
	def before_insert(self):
		self.sub_supplier()
		self.add_doc_name_as_supplier_number()

	def before_validate(self):
		self.check_confirmation_checkbox()

	def before_save(self):
		if self.is_data_confirmed == True:
			self.status = "Confirmed"

	def on_update(self):
		self.create_new_employee()
		self.add_main_employee_to_cht()

	def create_new_employee(self):
		is_employee_registered = frappe.get_list("Supplier Employee", filters={'email': self.main_contact_employee_email} , fields=["name"], pluck="name")
		if not is_employee_registered:
			new_employee = frappe.new_doc("Supplier Employee")
			# new_employee.status = "Raw Data"
			new_employee.is_main_contact = 1
			new_employee.supplier_company = self.name
			new_employee.last_name = self.main_contact_employee_last_name
			new_employee.first_name = self.main_contact_employee_first_name
			new_employee.email = self.main_contact_employee_email
			new_employee.phone_number = self.main_contact_employee_phone_number
			new_employee.position = self.main_contact_employee_position
			new_employee.insert()

	def add_main_employee_to_cht(self):
		main_contact = frappe.get_list("Supplier Employee", filters={'email': self.main_contact_employee_email} , fields=["name"], pluck="name")
		employee_list = [child.employee_email for child in self.employees if child.employee_email == self.main_contact_employee_email]
		if self.main_contact_employee_email not in employee_list:
			self.append("employees", {
				"employee_number": main_contact[0],
				"is_main_contact": 1
			})
			self.save()


	def sub_supplier(self):
		try:
			user = frappe.session.user
			user_doc = frappe.get_doc("User", user)
			# frappe.msgprint(f"User: {user}")

			try:
				user_supplier = frappe.db.get_value("Supplier Employee", {'email': user}, ['supplier_company'])
				# frappe.msgprint(f"User Supplier: {user_supplier}")
				user_supplier_number = frappe.db.get_value("Supplier", user_supplier, 'supplier_number')
			except:
				frappe.throw("Cannot find your supplier number. Please contact the system administrator.")
			try:
				original_parent_supplier_number = frappe.db.get_value("Supplier", user_supplier, 'original_parent_supplier_number')
				# frappe.msgprint(f"Tired Original Parent Supplier Number: {original_parent_supplier_number}")
			except:
				original_parent_supplier_number = None
			if not original_parent_supplier_number:
				original_parent_supplier_number = user_supplier_number
				# frappe.msgprint(f"After if not: Original Parent Supplier Number: {original_parent_supplier_number}")
			try:
				direct_parent_sub_supplier_level = frappe.db.get_value("Supplier", user_supplier, 'sub_supplier_level')
				# frappe.msgprint(f"Direct Parent Sub Supplier Level: {direct_parent_sub_supplier_level}")
			except:
				direct_parent_sub_supplier_level = None

			if direct_parent_sub_supplier_level is None:
				direct_parent_sub_supplier_level = 0
				# frappe.msgprint(f"After if none: Direct Parent Sub Supplier Level: {direct_parent_sub_supplier_level}")

			self.sub_supplier_level = direct_parent_sub_supplier_level + 1

			self.original_parent_supplier_number = original_parent_supplier_number
			# frappe.msgprint(f"Original Parent Supplier Number: {original_parent_supplier_number}")
			self.direct_parent_supplier = user_supplier
			# frappe.msgprint(f"Direct Parent Supplier: {user_supplier}")
			self.supplier_number = f"{direct_parent_sub_supplier_level + 1}S-{original_parent_supplier_number}"
			# frappe.msgprint(f"Supplier Number: {self.supplier_number}")
		except Exception as e:
			# Log any errors encountered
			frappe.log_error(message=str(e), title="Error processing supplier number")


	def add_doc_name_as_supplier_number(self):
		if not self.supplier_number:
			self.supplier_number = self.name


	def check_confirmation_checkbox(self):
		user_email = frappe.session.user
		try:
			user = frappe.get_doc("User", user_email)
		except frappe.DoesNotExistError:
			frappe.throw(_("User not found"))
		roles = [role.role for role in user.roles]
		if "Supplier" in roles and self.status == "Sent for confirmation" and self.is_data_confirmed != True:
			frappe.throw("Please check the 'Data Confirmed' checkbox before submitting the form.")