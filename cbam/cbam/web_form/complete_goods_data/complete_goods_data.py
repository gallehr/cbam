import frappe

def get_context(context):
	# do your magic here
	pass


@frappe.whitelist()
def get_filtered_supplier_employees(supplier, employee):
	employeeOptions = frappe.get_all("Supplier Employee Item", {"parenttype": "Supplier", "parentfield": "employees", "parent": supplier}, ["employee_number"],distinct=1)
	employeeOptions = [{"label": d.employee_number, "value": d.employee_number} for d in employeeOptions if d.employee_number != employee]
	return {
		"employeeOptions": employeeOptions,
	}

@frappe.whitelist() # Still needs to be tested
def get_suppliers_owned_by_supplier_employees(supplier):
	try:
		supplier_doc = frappe.get_doc("Supplier", supplier)
	except frappe.DoesNotExistError:
		frappe.throw(_("Supplier not found"))

	employee_list = [e.employee_number for e in supplier_doc.employees]
	supplier_options = []

	for e in employee_list:
		suppliers = frappe.get_all("Supplier", filters={"owner": e}, fields=["name"], pluck="name")
		supplier_options_list.extend(suppliers)

	supplier_options = [{"label": d.supplier_number, "value": d.supplier_number} for d in supplier_options_list]
	return {
		"supplier_options": supplier_options,
	}
