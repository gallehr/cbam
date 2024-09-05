import frappe
from frappe.core.doctype.communication.email import make

def send_email():
    is_data_confirmed_employee = frappe.db.get_single_value('Supplier Employee', 'enable_rent_reminders')
    if not is_reminder_enabled:
        print("not enabled")

    payment_details = frappe.get_all('Shop Rent Payment', fields=['status', 'due_date_of_payment', 'tenant_email', 'tenant_last_name'])

    for payment_detail in payment_details:
        if payment_detail['status'] == "Open" and payment_detail['tenant_email']:
            subject = "Rent Due Reminder"
            message = f"Dear {payment_detail['tenant_last_name']},\n\nThis is a friendly reminder that your rent is due on {payment_detail['due_date_of_payment']}. Please make sure to pay it on time to avoid any late fees.\n\nThank you."
            make(
                recipients=payment_detail['tenant_email'],
                sender=None,
                subject=subject,
                content=message,
                send_email=True
            )
