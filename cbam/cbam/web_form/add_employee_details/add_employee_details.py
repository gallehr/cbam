# import frappe

def get_context(context):
	pass

# @frappe.whitelist()
# def value_fetch():
# 	user = frappe.session.user
# 	supplier_employee_docname = frappe.get_all('Supplier Employee', filters={'email': user}, fields=['name'])
# 	if supplier_employee_docname:
# 		supplier = frappe.get_value('Supplier Employee', supplier_employee_docname[0].name, 'supplier_company')
# 	else:
# 		frappe.throw("We couldn't find to which supplier you belong to. Please contact ...")
# 	data = supplier
# 	return data
