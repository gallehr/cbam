# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Good(Document):
	def validate(self):
		self.get_main_contact_employee()
		self.split_good()

	def after_insert(self):
		self.add_to_linked_supplier_cht()
		self.add_to_linked_customs_import_cht()

	def before_save(self):
		if self.is_data_confirmed == True:
			self.status = "Done"

	def on_trash(self):
		self.delete_good_item()

	def get_main_contact_employee(self):
		if self.supplier and not self.employee:
			supplier_doc = frappe.get_doc("Supplier", self.supplier)
			for child in supplier_doc.employees:
				if child.is_main_contact == True:
					main_contact = child.employee_number
					self.employee = main_contact

	def split_good(self):
		if self.good_values == "Various Components":
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
				frappe.throw(f"The raw mass total of the components is not equal to the raw mass of the original good. <br><br> The total should be {original_raw_mass}, not {total_raw_mass}. <br><br> Please change the raw masses of the components and ensure that they add up to a total of {original_raw_mass}")
			else:
				self.status = "Done"
				if self.split_raw_mass_1 and self.split_raw_mass_1 != "0":
					new_good = frappe.new_doc("Good")
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
						# ToDo new_good.employee = self.employee
					else:
						frappe.throw("Please select a responsibility")
					new_good.insert()
					# self.append("good_splits", new_good) DOESN'T WORK
					# self.save()
					next_highest_split_number += 1
				if self.split_raw_mass_2 and self.split_raw_mass_2 != "0":
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
					new_good.raw_mass = self.split_raw_mass_2
					if self.responsibility_2 == "I'm the responsible Person":
						new_good.supplier = self.supplier
						new_good.employee = self.employee
					elif self.responsibility_2 == "Another employee is responsible":
						new_good.supplier = self.supplier
						new_good.employee = self.responsible_employee_2
					elif self.responsibility_2 == "Another supplier is responsible":
						new_good.supplier = self.responsible_supplier_2
						# ToDo new_good.employee = self.employee
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
						# ToDo new_good.employee = self.employee
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
						# ToDo new_good.employee = self.employee
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

	def add_to_linked_supplier_cht(self):
		supplier = frappe.get_doc("Supplier", self.supplier)
		supplier.append("goods", {
			"good_number": self.name
		})
		supplier.save()

	def add_to_linked_customs_import_cht(self):
		customs_import = frappe.get_doc("Customs Import", self.internal_customs_import_number)
		customs_import.append("goods", {
			"good_number": self.name
		})
		customs_import.save()

	def delete_good_item(self):
		supplier_item = frappe.get_all("Good Item", filters={'good_number': self.name}, fields=["name"], pluck="name")
		for item in supplier_item:
			item.delete()

@frappe.whitelist() # Called by Send Email button through goods.js
def create_new_supplier_user(good):
	frappe.msgprint(f"Good: {good}")
	employee_email = frappe.db.get_value("Supplier Employee", good.employee, "email")
	all_users_list = frappe.get_all("User", filters={'email': employee_email}, fields=["name"], pluck="name")
	if not all_users_list:
		employee_docname = frappe.db.get_value("Supplier Employee", good.employee, "name")
		employee_last_name = frappe.db.get_value("Supplier Employee", good.employee, "last_name")
		employee_first_name = frappe.db.get_value("Supplier Employee", good.employee, "first_name")
		frappe.db.set_value("Supplier Employee", employee_docname, "Status", "Sent to Supplier Employee")

		new_user = frappe.new_doc("User")
		new_user.email = employee_email
		new_user.last_name = employee_last_name
		new_user.first_name = employee_first_name
		new_user.append("role_profiles", {
			'role_profile': '00 Supplier',
		})
		new_user.insert()
		frappe.msgprint(f"New user {employee_email} created for {employee_last_name} {employee_first_name}")
	else:
		frappe.msgprint(f"User {employee_email} already exists")