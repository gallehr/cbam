import frappe
from frappe.core.doctype.communication.email import make


def create_email(recipient_employee):
    domain = "https://cbam-dev.frappe.cloud/"

    recipient_employee_email = frappe.db.get_value('Supplier Employee', recipient_employee, 'email')
    recipient_employee_last_name = frappe.db.get_value('Supplier Employee', recipient_employee, 'last_name')
    recipient_employee_supplier = frappe.db.get_value('Supplier Employee', recipient_employee, 'supplier_company')
    recipient_employee_owner = frappe.db.get_value('Supplier Employee', recipient_employee, 'owner')
    user_email = frappe.session.user
    is_user_supplier_employee = frappe.db.exists("Supplier Employee", {"email": user_email})

    # Hardcoded for testing purposes
    if not is_user_supplier_employee:
        sender_company = "Gallehr + Partner GmbH"
        sender_first_name = "Jon"
        sender_last_name = "Doe"
        sender_position = "CEO<br>"
        email_start_text = f"Dear Mr./Mrs. {recipient_employee_last_name},<br><br>Our company {sender_company} "
        email_end_text = f"<br><br>Best regards,<br>{sender_first_name} {sender_last_name}<br>{sender_position}{sender_company}"
    else:
        try:
            sender_employee_email = frappe.session.user
        except:
            frappe.throw("Couldn't find a user. Please contact the System Administrator.")
        sender_employee_list = frappe.get_all("Supplier Employee", filters={"email": sender_employee_email}, fields=["name"], pluck="name")
        if len(sender_employee_list) != 1:
            frappe.throw(f"An error occured. Number of found Supplier Employees: {len(sender_employee_list)} for user {sender_employee_email}. Please contact the System Administrator.")
        else:
            sender_supplier = frappe.db.get_value("Supplier Employee", sender_employee_list[0], "supplier_company")
            sender_company = frappe.db.get_value('Supplier', sender_supplier, 'supplier_name')
            sender_employee_first_name = frappe.db.get_value('Supplier Employee', sender_employee_list[0], 'first_name')
            sender_employee_last_name = frappe.db.get_value('Supplier Employee', sender_employee_list[0], 'last_name')
            sender_position = frappe.db.get_value('Supplier Employee', sender_employee_list[0], 'position')
            if not sender_position:
                sender_position = ""
            else:
                sender_position = f"{sender_position}<br>"
            email_start_text = f"DUMMY TEXT: <br>Dear Mr./Mrs. {recipient_employee_last_name},<br><br>I hope this email finds you well. I am forwarding the below request to you, as you are my Coworker/Sub-Supplier. To facilitate the process, I have created a user account for you, and kindly ask you to complete the three steps described below:<br><br>1. Registration<br>2. Access to data request<br>3. Data request<br><br>Thank you in advance for your cooperation, and I would appreciate it if you could address this at your earliest convenience. <br><br>Best regards,<br>{sender_employee_first_name} {sender_employee_last_name}<br>{sender_position}{sender_company}<br><br>----------------------------<br><br><em>Dear Mr./Mrs. {sender_employee_last_name},<br><br>Our company "
            email_end_text = "</em>"


    subject = f'CBAM - Confirmation of Data'

    message = f'{email_start_text}imports goods from you that are affected by the new European regulation Carbon Border Adjustment Mechanism (CBAM). We are legally required to provide detailed reports on the embedded CO2 emissions of CBAM goods we import from non-EU countries. To meet these reporting requirements, we need your assistance in collecting data. In order to ease the process for both sides we decided to utilize a CBAM data collection platform. This mail provides you with the registration link to this platform. On the platform you will be guided through the process and the platform will remember certain answers for the next round of data request, which will make it easier the next time around.<br><br>Please follow the steps outlined below:<br><br><strong>1. Registration:</strong><br>Click on <a href="{domain}login?redirect-to=%2Fapp%2Fwebsite#login-with-email-link" target="_blank">this link</a> and select the <strong>"Login with Email"</strong> button. Please use this email address, as it is the designated user account for you. <br><strong>2. Access to data request:</strong><br>After you completed the registration process, please, check your email inbox and click on the provided link.<br><strong>3. Data request:</strong><br>After logging in, please go through the Confirmation and Complete-Goods process.<br><br>We would appreciate it if you could complete these steps at your earliest convenience.<br><br>Thank you for your prompt attention to this matter.{email_end_text}'


    try:
        make(
            recipients=recipient_employee_email,
            sender=None,
            subject=subject,
            content=message,
            send_email=True
        )
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in sending email")
        frappe.msgprint("An error occurred while sending the email. Please check the error log for more details.")

    # For testing purposes
    frappe.msgprint(f"Email sent to {recipient_employee_email}:<br><br>{message}")