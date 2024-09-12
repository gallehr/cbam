# The `Supplier` class in the Python code creates a new user in the system based on supplier
# information when the status is "Sent to Supplier".
# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Supplier(Document):
	def before_insert(self):
		self.add_supplier_number_to_parent_field()
		self.add_doc_name_as_supplier_number()

	def on_update(self):
		self.create_new_employee()

	def after_insert(self):
		pass
		#self.add_main_contact_check_in_cht()

	def before_save(self):
		if self.is_data_confirmed == True:
			self.status = "Confirmed"


	def create_new_employee(self):
		is_employee_registered = frappe.get_list("Supplier Employee", filters={'email': self.main_contact_employee_email} , fields=["name"], pluck="name")
		if not is_employee_registered:
			new_employee = frappe.new_doc("Supplier Employee")
			new_employee.status = "Raw Data"
			new_employee.is_main_contact = 1
			new_employee.supplier_company = self.name
			new_employee.last_name = self.main_contact_employee_last_name
			new_employee.first_name = self.main_contact_employee_first_name
			new_employee.email = self.main_contact_employee_email
			new_employee.phone_number = self.main_contact_employee_phone_number
			new_employee.position = self.main_contact_employee_position
			new_employee.insert()
		# else:
		# 	frappe.msgprint("Employee already exists - Please contact your administrator")

	# def add_main_employee_to_cht(self):
	# 	main_contact = frappe.get_list("Supplier Employee", filters={'email': self.main_contact_employee_email} , fields=["name"], pluck="name")
	# 	employee_list = [child.employee_email for child in self.employees if child.employee_email == self.main_contact_employee_email]
	# 	if self.main_contact_employee_email not in employee_list:
	# 		self.append("employees", {
	# 			"employee_number": main_contact[0],
	# 			"is_main_contact": 1
	# 		})
	# 		self.save()

	# def add_main_contact_check_in_cht(self):
	# 	for child in self.employees:
	# 		if child.employee_email == self.main_contact_employee_email:
	# 			child.is_main_contact = 1
	# 			self.save()

	def add_supplier_number_to_parent_field(self): #STILL HAS TO BE TESTED WHEN SUPPLIER ADDS AN SUPPLIER
		try:
			user = frappe.session.user
			user_doc = frappe.get_doc("User", user)

			# Ensure role_profiles exists and is a list
			role_profiles = user_doc.get('role_profiles', [])
			if role_profiles:
				user_role_profiles_list = [profile.get('role_profile') for profile in role_profiles]

				if "00 Supplier" in user_role_profiles_list:
					supplier = frappe.db.get_value("Supplier Employee", {'email': user_doc.get('email')}, ['supplier_company'])
					self.parent_supplier = supplier
					user_doc.save()

		except Exception as e:
			# Log any errors encountered
			frappe.log_error(message=str(e), title="Error processing supplier number")


	def add_doc_name_as_supplier_number(self):
		if not self.supplier_number:
			self.supplier_number = self.name