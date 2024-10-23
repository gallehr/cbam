import frappe
no_cache = 1

def get_context(context):
    context.user = frappe.session.user
    context.employee_list = frappe.db.get_all('Supplier Employee', filters={'email': context.user}, fields=['name'], pluck="name")
    try:
        context.employee = context.employee_list[0]
        context.supplier = frappe.db.get_value('Supplier Employee', {'email': context.user}, 'supplier_company')
        context.supplier_doc = frappe.get_doc('Supplier', context.supplier)

        context.is_employee_main_contact = frappe.db.get_value("Supplier Employee", context.employee, "is_main_contact")

        context.is_employee_data_confirmed = frappe.db.get_value('Supplier Employee', context.employee, 'is_data_confirmed')
        context.is_supplier_data_confirmed = frappe.db.get_value('Supplier', context.supplier, 'is_data_confirmed')
        context.goods_list = frappe.get_all('Good', filters={'employee': context.employee}, fields=['status'], pluck="status") or []
        if any(status in context.goods_list for status in ["Raw Data", "Sent for completing"]):
            context.is_some_good_pending = True
        else:
            context.is_some_good_pending = False
    except IndexError:
        context.employee = "No employee found"
