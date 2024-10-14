import frappe
from frappe.core.doctype.communication.email import make
import json


@frappe.whitelist()  # Called by Send Email button through goods.js
def create_new_supplier_user(employee):
    #frappe.msgprint(f"Creating new user for {employee}")
    employee_email = frappe.db.get_value("Supplier Employee", employee, "email")
    users_list = frappe.get_all("User", filters={'email': employee_email}, fields=["name"], pluck="name")
    if not users_list:
        employee_docname = frappe.db.get_value("Supplier Employee", employee, "name")
        employee_last_name = frappe.db.get_value("Supplier Employee", employee, "last_name")
        employee_first_name = frappe.db.get_value("Supplier Employee", employee, "first_name") or employee_last_name
        frappe.db.set_value("Supplier Employee", employee_docname, "Status", "Sent to Supplier Employee")

        new_user = frappe.new_doc("User")
        new_user.email = employee_email
        new_user.send_welcome_email = 0
        new_user.last_name = employee_last_name
        new_user.first_name = employee_first_name

        # Ensure role_profiles child table is initialized
        try:
            new_user.append("role_profiles", {
                'role_profile': '00 Supplier',
            })
        except AttributeError:
            new_user.role_profile_name = "00 Supplier"

        new_user.insert()
