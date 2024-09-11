import frappe
no_cache = 1

def get_context(context):
    context.test = frappe.get_value('Supplier Employee', "EMP-078-00000007", "supplier_company")
    context.user = frappe.session.user
    # context.employee = frappe.db.get_value('Supplier Employee', filters={'email': context.user}, fields=['name'], pluck="name")
    # context.supplier = frappe.db.get_value('Supplier Employee', {'email': context.user}, 'supplier_company')
    # context.supplier_doc = frappe.get_doc('Supplier', context.supplier)
    
    
    # context.is_employee_main_contact
    
    # context.is_employee_data_confirmed = frappe.db.get_value('Supplier Employee', {'email': context.user}, 'is_data_confirmed')
    # context.is_supplier_data_confirmed = frappe.db.get_value('Supplier', context.supplier, 'is_data_confirmed')


    
    # def create_email(good, supplier):
    # domain = "https://cbam-dev.frappe.cloud/"
    # employee = frappe.db.get_value("Good", good, "employee")
    # is_data_confirmed_employee = frappe.db.get_value('Supplier Employee', employee, 'is_data_confirmed')
    # employee_email = frappe.db.get_value('Supplier Employee', employee, 'email')
    # employee_last_name = frappe.db.get_value('Supplier Employee', employee, 'last_name')
    # is_data_confirmed_supplier = frappe.db.get_value('Supplier', supplier, 'is_data_confirmed')
    # supplier_doc = frappe.get_doc("Supplier", supplier)
    # main_contact = [child.employee_number for child in supplier_doc.employees if child.is_main_contact]
    # if employee in main_contact:
    #     is_employee_main_contact = True
    # else:
    #     is_employee_main_contact = False
