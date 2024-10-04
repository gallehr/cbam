# Copyright (c) 2024, phamos GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import uuid

class CBAMInstallation(Document):
	def before_naming(self):
		self.generated_uuid()

	def before_validate(self):
		self.add_same_contact_person()

	def after_insert(self):
		self.add_to_operating_company_cht()

	def on_trash(self):
		self.delete_child_from_operating_company_cht()

	def generated_uuid(self):
		generated_uuid = uuid.uuid4()
		self.uuid_installation = generated_uuid

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