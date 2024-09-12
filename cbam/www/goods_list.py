import frappe
no_cache = 1

def get_context(context):
    context.user = frappe.session.user
    context.employee_list = frappe.db.get_all('Supplier Employee', filters={'email': context.user}, fields=['name'], pluck="name")
    context.employee = context.employee_list[0]
    context.goods_list = frappe.get_all('Good', filters={'employee': context.employee}, fields=['name', 'status', 'master_reference_number_mrn', 'good_description', 'article_number'])