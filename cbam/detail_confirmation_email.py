import frappe
from frappe.core.doctype.communication.email import make
import json

@frappe.whitelist()
def send_email(goods_list): #NOT TESTED COMPLETELY
    domain = "https://cbam-dev.frappe.cloud/"
    try:
        all_goods = json.loads(goods_list)
        for item in all_goods:
            if item['sent_to_employee'] == 'Not Sent':
                good = item['good_number']
                supplier = item['supplier']
                create_email(good, supplier)
    except json.JSONDecodeError:
        good = goods_list
        supplier = frappe.get_value('Good', good, 'supplier')
        create_email(good, supplier)

def create_email(good, supplier):
    frappe.set_value('Good', good, 'sent_to_supplier_employee', 'Sent')
    employee = frappe.get_value("Good", good, "employee")
    is_data_confirmed_employee = frappe.db.get_value('Supplier Employee', employee, 'is_data_confirmed')
    employee_email = frappe.get_value('Supplier Employee', employee, 'email')
    employee_last_name = frappe.get_value('Supplier Employee', employee, 'last_name')
    is_data_confirmed_supplier = frappe.get_value('Supplier', supplier, 'is_data_confirmed')
    supplier_doc = frappe.get_doc("Supplier", supplier)
    main_contact = [child.employee_number for child in supplier_doc.employees if child.is_main_contact]
    if employee in main_contact:
        is_employee_main_contact = True
    else:
        is_employee_main_contact = False

    # Email creation depending on the data confirmation status
    subject = f'CBAM - Confirmation of Data'

    message_start = f'Dear Mr./Mrs. {employee_last_name},\n\nThank you for our continued collaboration. In light of the new European regulation, CBAM, we kindly request your confirmation by following the steps outlined below:\n\n1. Click on this link: {domain}login?redirect-to=%2Fapp%2Fwebsite#login-with-email-link and select the "Login with Email" button. Please use this email address, as it is the designated user account for you. \n2. Check your email inbox and click on the link provided in the email you receive.\n\nAfter logging in:\n\n'

    if not is_data_confirmed_supplier and is_employee_main_contact:
        message_confirm_supplier = f"- Please verify and confirm the data we have for your company by clicking on the following link:  {domain}confirm-supplier-details/{supplier}/edit\n\n"
        frappe.set_value('Supplier', supplier, 'status', "Sent for confirmation")
    else:
        message_confirm_supplier = ""

    if not is_data_confirmed_employee:
        message_confirm_employee = f"- Please verify and confirm that your personal information is correct by clicking on the following link: {domain}confirm-employee-details/{employee}/edit\n\n"
    else:
        message_confirm_employee = ""

    message_end = f"- Review the list of goods we purchased from you, click each item, and update it with the required information. The list can be found by clicking this link: {domain}complete-goods-data/list\n\nWe would appreciate it if you could complete these steps at your earliest convenience.\n\nThank you for your prompt attention to this matter.\n\nBest regards,\n\n[Your Name]\n[Your Position]\n[Your Company Name]"

    frappe.msgprint(f"Email sent to {employee_email}")

    # make(
    #     recipients=employee_email,
    #     sender=None,
    #     subject=subject,
    #     content= message_start + message_confirm_supplier + message_confirm_employee + message_end,
    #     send_email=True
    # )
