import frappe
from cbam.send_email.create_email import create_email
from cbam.send_email.create_new_supplier_user import create_new_supplier_user
from frappe.core.doctype.communication.email import make
import json

@frappe.whitelist()
def send_email(good):
    supplier = frappe.db.get_value('Good', good, 'supplier')
    employee = frappe.db.get_value("Good", good, "employee")
    try:
        create_new_supplier_user(employee)
        create_email(employee)
        supplier_doc = frappe.get_doc("Supplier", supplier)
        frappe.db.set_value("Supplier Employee", employee, "status", "Sent to Supplier Employee")
        for good in supplier_doc.goods:
            frappe.db.set_value('Good', good.good_number, 'status', 'Sent for completing')
        is_employee_main_contact = frappe.db.get_value('Supplier Employee', employee, 'is_main_contact')
        if is_employee_main_contact:
            frappe.db.set_value('Supplier', supplier, 'status', "Sent for confirmation")
    except Exception as e:
        frappe.throw(f"Couldn't send Email. Please contact the System Administrator. <br><br>Error: {e}")
