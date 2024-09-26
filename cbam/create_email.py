import frappe
from frappe.core.doctype.communication.email import make


def create_email(employee):
    # frappe.msgprint(f"Good: {good}, Supplier: {supplier}")
    domain = "https://cbam-dev.frappe.cloud/"
    # supplier_doc = frappe.get_doc("Supplier", supplier)
    # for good in supplier_doc.goods:
    #     frappe.db.set_value('Good', good.good_number, 'sent_to_supplier_employee', 'Sent')
    # employee = frappe.db.get_value("Good", good, "employee")
    #is_data_confirmed_employee = frappe.db.get_value('Supplier Employee', employee, 'is_data_confirmed')
    employee_email = frappe.db.get_value('Supplier Employee', employee, 'email')
    employee_last_name = frappe.db.get_value('Supplier Employee', employee, 'last_name')
    # is_employee_main_contact = frappe.db.get_value('Supplier Employee', employee, 'is_main_contact')
    # if is_employee_main_contact:
    #     frappe.db.set_value('Supplier', supplier, 'status', "Sent for confirmation")


    subject = f'CBAM - Confirmation of Data'

    message = f'Dear Mr./Mrs. {employee_last_name},<br><br>Thank you for our continued collaboration. In light of the new European regulation, CBAM, we kindly request your confirmation by following the steps outlined below:<br><br>1. Click on this <a href="{domain}login?redirect-to=%2Fapp%2Fwebsite#login-with-email-link" target="_blank">link</a> and select the "Login with Email" button. Please use this email address, as it is the designated user account for you. <br>2. Check your email inbox and click on the link provided in the email you receive.<br><br>After logging in, please go throgh the Confirmation and Complete-Goods process.<br><br>We would appreciate it if you could complete these steps at your earliest convenience.<br><br>Thank you for your prompt attention to this matter.<br><br>Best regards,<br>[John Doe]<br>[Procurement Manager]<br>[Company XYZ]'


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

    # For testing purposes
    frappe.msgprint(f"Email sent to {employee_email}:<br><br>{message}")