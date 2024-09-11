import frappe
no_cache = 1

def get_context(context):
    context.test = frappe.get_value('Supplier Employee', "EMP-078-00000007", "supplier_company")