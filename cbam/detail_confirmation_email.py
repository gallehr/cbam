import frappe
from frappe.core.doctype.communication.email import make

def send_email(supplier, employee):
    is_data_confirmed_employee = frappe.db.get_single_value('Supplier Employee', employee, 'is_data_confirmed')
    employee_email = frappe.get_value('Supplier Employee', employee, 'email')
    employee_last_name = frappe.get_value('Supplier Employee', employee, 'last_name')
    is_data_confirmed_supplier = frappe.get_value('Supplier', supplier, 'is_data_confirmed')
    supplier_doc = frappe.get_doc("Supplier", supplier)
    main_contact = [supplier_doc.employee_number for child in supplier_doc.employees if child.is_main_contact]
    if employee in main_contact:
        is_employee_main_contact = True
    else:
        is_employee_main_contact = False

    subject = f'CBAM - Confirmation of Data'

    message_start = f'Dear Mr./Mrs. {employee_last_name},\n\nThank you for our continued collaboration.\n\nIn light of the new European regulation CBAM, we require your confirmation. Please follow the steps outlined below:\n\n1. Click on [this link](http://127.0.0.1:8000/login?redirect-to=%2Fapp%2Fwebsite#login-with-email-link) and select the "Login with Email" button. Please use this email address, as it is the designated user account for you.\n2. Return to your email inbox and click on the link provided in the email you receive.\n\nAfter the login process:\n\n'

    if not is_data_confirmed_supplier and is_employee_main_contact:
        message_confirm_supplier = f"- Please check and confirm that the data we have of your Company by clicking on the following link: https://fuzzy-fortnight-7j67vp54w6rf74-8000.app.github.dev/confirm-supplier-details/{supplier}/edit\n\n"
    else:
        message_confirm_supplier = ""

    if not is_data_confirmed_employee:
        message_confirm_employee = f"- Please check and confirm that the data we have of you is correct by clicking on the following link: https://fuzzy-fortnight-7j67vp54w6rf74-8000.app.github.dev/confirm-employee-details/{employee}/edit\n\n"
    else:
        message_confirm_employee = ""

    message_end = f"- Please go through the following list of Goods we boutht from you, click it and edit it one by one, and add the required data. You will find the list by clicking on the following link: https://fuzzy-fortnight-7j67vp54w6rf74-8000.app.github.dev/complete-goods-data/list\n\nWe would appreciate if you complete these steps at your earliest convenience.\n\nThank you for your prompt attention to this matter.\n\nBest regards,\n\n[Your Name]\n[Your Position]\n[Your Company Name]"

    frappe.msgprint(message_start + message_confirm_supplier + message_confirm_employee + message_end)

    make(
        recipients=employee_email,
        sender=None,
        subject=subject,
        content= message_start + message_confirm_supplier + message_confirm_employee + message_end,
        send_email=True
    )
