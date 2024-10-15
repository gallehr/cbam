# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from cbam.send_email.create_email import create_email
from cbam.send_email.create_new_supplier_user import create_new_supplier_user

class Good(Document):
	# def before_validate(self):
	# 	self.check_confirmation_checkbox()

	def validate(self):
		self.split_good()

	def before_save(self):
		self.delete_old_employee_if_supplier_changed()
		self.get_main_contact_employee()
		if self.is_data_confirmed == True and self.manufacture == "I am the manufacture":
			self.status = "Done"
		self.add_to_supplier_cht()
		self.add_to_employee_cht()
		self.add_to_customs_import_cht()

	def on_update(self):
		self.add_split_good_to_parent_cht()
		self.send_email()

	def on_trash(self):
		self.delete_all_good_item()

	def delete_old_employee_if_supplier_changed(self):
		has_supplier_changed = self.has_value_changed("supplier")
		if has_supplier_changed:
			self.employee = None

	def get_main_contact_employee(self):
		if self.supplier and not self.employee:
			supplier_doc = frappe.get_doc("Supplier", self.supplier)
			for child in supplier_doc.employees:
				if child.is_main_contact in ["1", 1, True]:
					main_contact = child.employee_number
					self.employee = main_contact

	def split_good(self):
		if self.manufacture == "I am NOT the manufacturer of the whole amount of the product":
			total_raw_mass = sum(
				getattr(self, attr, 0) or 0
				for attr in [
					'split_raw_mass_1',
					'split_raw_mass_2',
					'split_raw_mass_3',
					'split_raw_mass_4',
					'split_raw_mass_5'
				]
			)
			next_highest_split_number = 0
			if total_raw_mass != self.raw_mass:
				original_raw_mass = self.raw_mass
				frappe.throw(f"The raw mass total of the components is not equal to the raw mass of the original good. <br><br> The total should be {original_raw_mass}, not {total_raw_mass}. <br><br> Please change the raw masses of the components and ensure that they add up to a total of {original_raw_mass}.")
			else:
				self.status = "Split"
				if self.split_raw_mass_1 and self.split_raw_mass_1 != "0":
					new_good = frappe.new_doc("Good")
					new_good.parent_good = self.name
					new_good.master_reference_number_mrn = self.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
					new_good.hand_over_date = self.hand_over_date
					new_good.article_number = self.article_number
					new_good.customs_tariff_number = self.customs_tariff_number
					new_good.good_description = self.good_description
					new_good.internal_customs_import_number = self.internal_customs_import_number
					new_good.country_of_origin = self.country_of_origin
					new_good.shipping_country = self.shipping_country
					new_good.customs_procedure = self.customs_procedure
					new_good.raw_mass = self.split_raw_mass_1
					if self.responsibility_1 == "I'm the responsible Person":
						new_good.supplier = self.supplier
						new_good.employee = self.employee
					elif self.responsibility_1 == "Another employee is responsible":
						new_good.supplier = self.supplier
						new_good.employee = self.responsible_employee_1
					elif self.responsibility_1 == "Another supplier is responsible":
						new_good.supplier = self.responsible_supplier_1
					else:
						frappe.throw("Please select a responsibility")
					new_good.insert()
					next_highest_split_number += 1
				if self.split_raw_mass_2 and self.split_raw_mass_2 != "0":
					new_good = frappe.new_doc("Good")
					new_good.parent_good = self.name
					new_good.master_reference_number_mrn = self.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
					new_good.hand_over_date = self.hand_over_date
					new_good.article_number = self.article_number
					new_good.good_description = self.good_description
					new_good.internal_customs_import_number = self.internal_customs_import_number
					new_good.customs_tariff_number = self.customs_tariff_number
					new_good.country_of_origin = self.country_of_origin
					new_good.shipping_country = self.shipping_country
					new_good.customs_procedure = self.customs_procedure
					new_good.raw_mass = self.split_raw_mass_2
					if self.responsibility_2 == "I'm the responsible Person":
						new_good.supplier = self.supplier
						new_good.employee = self.employee
					elif self.responsibility_2 == "Another employee is responsible":
						new_good.supplier = self.supplier
						new_good.employee = self.responsible_employee_2
					elif self.responsibility_2 == "Another supplier is responsible":
						new_good.supplier = self.responsible_supplier_2
					else:
						frappe.throw("Please select a responsibility")
					new_good.insert()
					next_highest_split_number += 1
				if self.split_raw_mass_3 and self.split_raw_mass_3 != "0":
					new_good = frappe.new_doc("Good")
					new_good.master_reference_number_mrn = self.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
					new_good.hand_over_date = self.hand_over_date
					new_good.article_number = self.article_number
					new_good.good_description = self.good_description
					new_good.internal_customs_import_number = self.internal_customs_import_number
					new_good.customs_tariff_number = self.customs_tariff_number
					new_good.country_of_origin = self.country_of_origin
					new_good.shipping_country = self.shipping_country
					new_good.customs_procedure = self.customs_procedure
					new_good.raw_mass = self.split_raw_mass_3
					if self.responsibility_3 == "I'm the responsible Person":
						new_good.supplier = self.supplier
						new_good.employee = self.employee
					elif self.responsibility_3 == "Another employee is responsible":
						new_good.supplier = self.supplier
						new_good.employee = self.responsible_employee_3
					elif self.responsibility_3 == "Another supplier is responsible":
						new_good.supplier = self.responsible_supplier_3
					else:
						frappe.throw("Please select a responsibility")
					new_good.insert()
					next_highest_split_number += 1
				if self.split_raw_mass_4 and self.split_raw_mass_4 != "0":
					new_good = frappe.new_doc("Good")
					new_good.master_reference_number_mrn = self.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
					new_good.hand_over_date = self.hand_over_date
					new_good.article_number = self.article_number
					new_good.good_description = self.good_description
					new_good.internal_customs_import_number = self.internal_customs_import_number
					new_good.customs_tariff_number = self.customs_tariff_number
					new_good.country_of_origin = self.country_of_origin
					new_good.shipping_country = self.shipping_country
					new_good.customs_procedure = self.customs_procedure
					new_good.raw_mass = self.split_raw_mass_4
					if self.responsibility_4 == "I'm the responsible Person":
						new_good.supplier = self.supplier
						new_good.employee = self.employee
					elif self.responsibility_4 == "Another employee is responsible":
						new_good.supplier = self.supplier
						new_good.employee = self.responsible_employee_4
					elif self.responsibility_4 == "Another supplier is responsible":
						new_good.supplier = self.responsible_supplier_4
					else:
						frappe.throw("Please select a responsibility")
					new_good.insert()
					next_highest_split_number += 1
				if self.split_raw_mass_5 and self.split_raw_mass_5 != "0":
					new_good = frappe.new_doc("Good")
					new_good.master_reference_number_mrn = self.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
					new_good.hand_over_date = self.hand_over_date
					new_good.article_number = self.article_number
					new_good.good_description = self.good_description
					new_good.internal_customs_import_number = self.internal_customs_import_number
					new_good.customs_tariff_number = self.customs_tariff_number
					new_good.country_of_origin = self.country_of_origin
					new_good.shipping_country = self.shipping_country
					new_good.customs_procedure = self.customs_procedure
					new_good.raw_mass = self.split_raw_mass_5
					if self.responsibility_5 == "I'm the responsible Person":
						new_good.supplier = self.supplier
						new_good.employee = self.employee
					elif self.responsibility_5 == "Another employee is responsible":
						new_good.supplier = self.supplier
						new_good.employee = self.responsible_employee_5
					elif self.responsibility_5 == "Another supplier is responsible":
						new_good.supplier = self.responsible_supplier_5
						# ToDo new_good.employee = self.employee
					else:
						frappe.throw("Please select a responsibility")
					new_good.insert()
					next_highest_split_number += 1

	def add_to_supplier_cht(self):
		has_supplier_changed = self.has_value_changed("supplier")
		if has_supplier_changed:
			delete_good_item(self.name, "Supplier")
			supplier = frappe.get_doc("Supplier", self.supplier)
			supplier.append("goods", {
				"good_number": self.name,
				"supplier": self.supplier,
				"employee": self.employee,
				"status": self.status
			})
			supplier.save()

	def add_to_employee_cht(self):
		has_employee_changed = self.has_value_changed("employee")
		if has_employee_changed:
			delete_good_item(self.name, "Supplier Employee")
			employee = frappe.get_doc("Supplier Employee", self.employee)
			employee.append("goods", {
				"good_number": self.name,
				"supplier": self.supplier,
				"employee": self.employee,
				"status": self.status
			})
			employee.save()

	def add_to_customs_import_cht(self):
		has_internal_customs_import_number_changed = self.has_value_changed("internal_customs_import_number")
		if has_internal_customs_import_number_changed:
			delete_good_item(self.name, "Customs Import")
			customs_import = frappe.get_doc("Customs Import", self.internal_customs_import_number)
			customs_import.append("goods", {
				"good_number": self.name,
				"supplier": self.supplier,
				"employee": self.employee,
				"status": self.status
			})
			customs_import.save()

	def add_split_good_to_parent_cht(self):
		if self.parent_good:
			new_good_item = frappe.new_doc("Good Item")
			new_good_item.parenttype = "Good"
			new_good_item.parent = self.parent_good
			new_good_item.parentfield = "good_components"
			new_good_item.good_number = self.name
			new_good_item.supplier = self.supplier
			new_good_item.employee = self.employee
			new_good_item.insert()

	def delete_all_good_item(self):
		good_items = frappe.get_all("Good Item", filters={'good_number': self.name}, fields=["name"], pluck="name")
		for good_item in good_items:
			frappe.db.delete("Good Item", {
				"name": good_item
			})
		frappe.db.commit()

	def check_confirmation_checkbox(self):
		# if no attribute __unsaved means, the document is updated through a Web Form because only then (update + web form) self doesn't have this attribute
		if not hasattr(self, '__unsaved'):
			user_email = frappe.session.user
			# frappe.msgprint(f"User Email: {user_email}")
			try:
				user = frappe.get_doc("User", user_email)
				# frappe.msgprint(f"User: {user}")
			except frappe.DoesNotExistError:
				frappe.throw(_("User not found"))
			role_list = [r.role for r in user.roles]
			if "Supplier" in role_list:
				# frappe.msgprint("User is a supplier")
				# frappe.msgprint(f"is data confirmed{self.is_data_confirmed}")
				if self.is_data_confirmed != True:
					frappe.throw("Please check the 'Data Confirmed' checkbox before submitting the form.")

	def send_email(self):
		employee_goods_status_list = frappe.get_all("Good", filters={'employee': self.employee}, fields=["status"], pluck="status")
		if all(status == "Done" for status in employee_goods_status_list):
			owner_employee_email = frappe.db.get_value("Supplier Employee", self.employee, "email")
			new_employee_list = frappe.get_all("Supplier Employee", filters={'owner': self.employee}, fields=["name"], pluck="name")
			frappe.msgprint(f"New Employee List: {new_employee_list}")
			for employee in new_employee_list:
				try:
					create_new_supplier_user(employee)
				except Exception as e:
					frappe.msgprint ("Couldn't create a new user for the employee {employee}.<br><br>Error: {e}")
				try:
					create_email(employee)
				except Exception as e:
					frappe.msgprint ("Couldn't create an email for the employee {employee}.<br><br>Error: {e}")

def delete_good_item(good, parenttype):
	good_item_list = frappe.get_all("Good Item", filters={'good_number': good, 'parenttype': parenttype}, fields=["name"], pluck="name")
	good_item = ', '.join(good_item_list)
	frappe.db.delete("Good Item", {
		"name": good_item
	})
	frappe.db.commit()