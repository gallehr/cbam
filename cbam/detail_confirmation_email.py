import frappe
from frappe.core.doctype.communication.email import make
import json

@frappe.whitelist()
def send_email(goods_list):
    # frappe.msgprint(f"Goods list: {goods_list}")
    try:
        all_goods = json.loads(goods_list)
        for item in all_goods:
            if item['sent_to_employee'] == 'Not Sent':
                good = item['good_number']
                supplier = item['supplier']
                frappe.enqueue(create_email, queue='default', param1=good, param2=supplier)
    except json.JSONDecodeError:
        good = goods_list
        sending_status = frappe.db.get_value('Good', good, 'sent_to_supplier_employee')
        if sending_status == 'Not sent':
            supplier = frappe.db.get_value('Good', good, 'supplier')
            create_email(good, supplier)
        else:
            frappe.msgprint(f"Email already sent for good {good}")

def create_email(good, supplier):
    # frappe.msgprint(f"Good: {good}, Supplier: {supplier}")
    domain = "https://cbam-dev.frappe.cloud/"
    supplier_doc = frappe.get_doc("Supplier", supplier)
    for good in supplier_doc.goods:
        frappe.db.set_value('Good', good.good_number, 'sent_to_supplier_employee', 'Sent')
    employee = frappe.db.get_value("Good", good, "employee")
    #is_data_confirmed_employee = frappe.db.get_value('Supplier Employee', employee, 'is_data_confirmed')
    employee_email = frappe.db.get_value('Supplier Employee', employee, 'email')
    employee_last_name = frappe.db.get_value('Supplier Employee', employee, 'last_name')
    is_employee_main_contact = frappe.db.get_value('Supplier Employee', employee, 'is_main_contact')
    if is_employee_main_contact:
        frappe.db.set_value('Supplier', supplier, 'status', "Sent for confirmation")
    #is_data_confirmed_supplier = frappe.db.get_value('Supplier', supplier, 'is_data_confirmed')
    #supplier_doc = frappe.get_doc("Supplier", supplier)
    #main_contact = [child.employee_number for child in supplier_doc.employees if child.is_main_contact]
    # if employee in main_contact:
    #     is_employee_main_contact = True
    # else:
    #     is_employee_main_contact = False


    subject = f'CBAM - Confirmation of Data'

    message_start = f'Dear Mr./Mrs. {employee_last_name},<br><br>Thank you for our continued collaboration. In light of the new European regulation, CBAM, we kindly request your confirmation by following the steps outlined below:<br><br>1. Click on this <a href="{domain}login?redirect-to=%2Fapp%2Fwebsite#login-with-email-link" target="_blank">link</a> and select the "Login with Email" button. Please use this email address, as it is the designated user account for you. <br>2. Check your email inbox and click on the link provided in the email you receive.<br><br>After logging in, please go throgh the Confirmation and Complete-Goods process.<br><br>We would appreciate it if you could complete these steps at your earliest convenience.<br><br>Thank you for your prompt attention to this matter.<br><br>Best regards,<br>[John Doe]<br>[Procurement Manager]<br>[Company XYZ]'

    # if not is_data_confirmed_supplier and is_employee_main_contact:
    #     message_confirm_supplier = f'- Please verify and confirm the data we have for your company by clicking on this <a href="{domain}confirm-supplier-data/{supplier}/edit" target="_blank">link</a>.<br>'
    #     frappe.db.set_value('Supplier', supplier, 'status', "Sent for confirmation")
    # else:
    #     message_confirm_supplier = ""

    # if not is_data_confirmed_employee:
    #     message_confirm_employee = f'- Please verify and confirm that your personal information is correct by clicking on this <a href="{domain}confirm-employee-details/{employee}/edit" target="_blank">link</a>.<br>'
    # else:
    #     message_confirm_employee = ""

    # message_end = f'- Review the list of goods we purchased from you, click each item, and update it with the required information. The list can be found by clicking this <a href="{domain}complete-goods-data/list" target="_blank">link</a>.<br><br>We would appreciate it if you could complete these steps at your earliest convenience.<br><br>Thank you for your prompt attention to this matter.<br><br>Best regards,<br>[John Doe]<br>[Procurement Manager]<br>[Company XYZ]'

    message = message_start # message_confirm_supplier + message_confirm_employee + message_end

    # For testing purposes
    frappe.msgprint(f"Email sent to {employee_email}:<br><br>{message}")


    try:
        make(
            recipients=employee_email,
            sender=None,
            subject=subject,
            content=message,
            send_email=True
        )
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in sending email")
        frappe.msgprint("An error occurred while sending the email. Please check the error log for more details.")
