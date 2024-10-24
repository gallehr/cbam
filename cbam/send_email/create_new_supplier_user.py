import frappe
from frappe.core.doctype.communication.email import make
import json


@frappe.whitelist()  # Called by Send Email button through goods.js
def create_new_supplier_user(employee):
    #frappe.msgprint(f"From create_new_supplier_user: Creating new user for {employee}")
    employee_doc = frappe.get_doc("Supplier Employee", employee)
    if not frappe.db.exists("User", employee_doc.email):

        try:
            new_user = frappe.new_doc("User")
            new_user.email = employee_doc.email
            new_user.send_welcome_email = False
            new_user.last_name = employee_doc.last_name
            new_user.first_name = employee_doc.first_name or employee_doc.last_name
            new_user.append("roles", {
                'role': 'Supplier'
            })
      
            new_user.save(ignore_permissions=True)
            frappe.db.set_value("Supplier Employee", employee_doc.name, "Status", "Sent to Supplier Employee")
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"An error occured while creating user for {employee_doc.name}")
       
