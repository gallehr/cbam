import frappe
from cbam.create_email import create_email
from cbam.create_new_supplier_user import create_new_supplier_user
import json

@frappe.whitelist()
def create_user_and_send_email(employee, supplier):
    good_list = frappe.get_all("Good", filters={"employee": employee}, fields=["name"], pluck="name")
    if good_list:
        try:
            create_new_supplier_user(employee)
            create_email(employee)
            frappe.db.set_value("Supplier Employee", employee, "status", "Sent to Supplier Employee")
            for good in good_list:
                frappe.db.set_value('Good', good, 'sent_to_supplier_employee', 'Sent')
            is_employee_main_contact = frappe.db.get_value('Supplier Employee', employee, 'is_main_contact')
            if is_employee_main_contact:
                frappe.db.set_value('Supplier', supplier, 'status', "Sent for confirmation")
        except Exception as e:
            frappe.throw(f"Couldn't send Email. Please contact the System Administrator. <br><br>Error: {e}")
    else:
        frappe.throw("No goods found for this employee. The Email only gets sent if the employee is linked to at least one good.")
