# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import uuid
from frappe.utils import cstr

class CBAMInstallation(Document):
	def before_naming(self):
		self.generated_uuid()

	def before_insert(self):
		self.set_operating_company()

	def before_validate(self):
		self.add_same_contact_person()

	def after_insert(self):
		self.add_to_operating_company_cht()

	def on_trash(self):
		self.delete_child_from_operating_company_cht()
		self.delete_link_in_good()

	def generated_uuid(self):

		self.uuid_installation =cstr(uuid.uuid4()) 

	def add_same_contact_person(self):
		has_contact_person_changed = self.has_value_changed("contact_person")
		has_operating_company_changed = self.has_value_changed("operating_company")
		if has_contact_person_changed:
			if self.contact_person == "Same contact person as Operating Company" and has_operating_company_changed:
				operating_company = frappe.get_doc("CBAM Operating Company", self.operating_company)
				self.first_name_same = operating_company.first_name
				self.last_name_same = operating_company.last_name
				self.email_same = operating_company.email
				self.phone_number_same = operating_company.phone_number
				self.position_same = operating_company.position_in_the_company
			elif self.contact_person == "Different contact person":
				self.first_name_same = ""
				self.last_name_same = ""
				self.email_same = ""
				self.phone_number_same = ""
				self.position_same = ""
			else:
				frappe.throw("Please select a valid contact person option")

	def add_to_operating_company_cht(self):
		has_operating_company_changed = self.has_value_changed("operating_company")
		if has_operating_company_changed:
			operating_company = frappe.get_doc("CBAM Operating Company", self.operating_company)
			operating_company.append("installations", {
				"cbam_installation": self.name,
			})
			operating_company.save()

	def delete_child_from_operating_company_cht(self):
		if self.operating_company:
			operating_company = frappe.get_doc("CBAM Operating Company", self.operating_company)
			for child in operating_company.installations:
				if child.cbam_installation == self.name:
					child.delete()

	def delete_link_in_good(self):
		linked_goods_list = frappe.get_all("Good", filters={"installation": self.name}, fields=["name"], pluck="name")
		for good in linked_goods_list:
			frappe.db.set_value("Good", good, "installation", "")

	def check_if_supplier_user(self):
		user_email = frappe.session.user
		#frappe.msgprint(str(user_email))
		try:
			user = frappe.get_doc("User", user_email)
		except frappe.DoesNotExistError:
			frappe.throw(_("User not found"))
		role_list = [r.role for r in user.roles]
		#frappe.msgprint(str(role_list))
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

	def set_operating_company(self):
		is_supplier_user, employee_list = self.check_if_supplier_user()
		if is_supplier_user:
			#frappe.throw(str(is_supplier_user))
			supplier = frappe.db.get_value("Supplier Employee", employee_list[0], "supplier_company")
			operating_company_list = frappe.db.get_all("CBAM Operating Company", filters={"parent_supplier": supplier}, fields=["name"], pluck="name")
			if len(operating_company_list) < 1:
				frappe.throw("No Operating Company found")
			if len(operating_company_list) > 1:
				frappe.throw("The supplier company of your User has more than one CBAM Operating Company. Please contact the system administrator.")
			else:
				self.operating_company = operating_company_list[0]
				try:
					uuid_operating_company_value = frappe.db.get_value("CBAM Operating Company", operating_company_list[0], "uuid")
					self.uuid_operating_company = uuid_operating_company_value
					self.parent_supplier = supplier
				except:
					frappe.throw("Cannot find a UUID or Parent Supplier for this CBAM Operating Company")
				#frappe.msgprint(str(operating_company_list[0]))
		else:
			frappe.throw("You are not registered as a supplier and therefore we cannot find the CBAM Operating Company. Please contact the system administrator.")