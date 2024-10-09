import frappe
from frappe.core.doctype.communication.email import make


def create_email(employee):
    domain = "https://cbam-dev.frappe.cloud/"
    sending_company = "Gallehr+Partner GmbH"

    employee_doc = frappe.get_doc('Supplier Employee', employee)

    #employee_email = frappe.db.get_value('Supplier Employee', employee, 'email')
    #employee_last_name = frappe.db.get_value('Supplier Employee', employee, 'last_name')
    
    #employee_supplier = frappe.db.get_value('Supplier Employee Item', filters={"employee_number": employee}, fields=["parent"], pluck="parent")
    supplier_name = frappe.db.get_value('Supplier', employee_doc.supplier_company, 'supplier_name')
    position = ""
    if employee_doc.position:
        position = f"{employee_doc.position}<br>"

    subject = f'CBAM - Confirmation of Data'

    message = f'Dear Mr./Mrs. {employee_doc.last_name},<br><br>Our company {supplier_name} imports goods from you that are affected by the new European regulation Carbon Border Adjustment Mechanism (CBAM). We are legally required to provide detailed reports on the embedded CO2 emissions of CBAM goods we import from non-EU countries. To meet these reporting requirements, we need your assistance in collecting data. In order to ease the process for both sides we decided to utilize a CBAM data collection platform. This mail provides you with the registration link to this platform. On the platform you will be guided through the process and the platform will remember certain answers for the next round of data request, which will make it easier the next time around.<br><br>Please follow the steps outlined below:<br><br><strong>1. Registration:</strong><br>Click on <a href="{domain}login?redirect-to=%2Fapp%2Fwebsite#login-with-email-link" target="_blank">this link</a> and select the <strong>"Login with Email"</strong> button. Please use this email address, as it is the designated user account for you. <br><strong>2. Access to data request:</strong><br>After you completed the registration process, please, check your email inbox and click on the provided link.<br><strong>3. Data request:</strong><br>After logging in, please go through the Confirmation and Complete-Goods process.<br><br>We would appreciate it if you could complete these steps at your earliest convenience.<br><br>Thank you for your prompt attention to this matter.<br><br>Best regards,<br>{employee_doc.first_name} {employee_doc.last_name}<br>{position}{supplier_name}'


    try:
        make(
            recipients=employee_doc.email,
            sender=f"{employee_doc.first_name} {employee_doc.last_name} - {sending_company}",
            subject=subject,
            content=message,
            send_email=True
        )
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in sending email")
        frappe.msgprint("An error occurred while sending the email. Please check the error log for more details.")

    # For testing purposes
    frappe.msgprint(f"Email sent to {employee_doc.email}:<br><br>{message}")