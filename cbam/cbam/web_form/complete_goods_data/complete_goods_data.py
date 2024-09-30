import frappe

def get_context(context):
	# do your magic here
	pass


@frappe.whitelist()
def get_filtered_supplier_employees(supplier, employee):
	frappe.msgprint(f"Employee Function works. Supplier: {supplier}, Employee: {employee}")
	# employeeOptions = frappe.get_all("Supplier Employee Item", {"parenttype": "Supplier", "parentfield": "employees", "parent": supplier}, ["employee_number"], distinct=1)
	supplier_doc = frappe.get_doc("Supplier", supplier)
	employeeOptions = [e.employee_number for e in supplier_doc.employees]
	frappe.msgprint(f"Employee Options: {employeeOptions}")
	employeeOptions = [{"label": d.employee_number, "value": d.employee_number} for d in employeeOptions if d.employee_number != employee]
	frappe.msgprint(f"Employee Options: {str(employeeOptions)}")
	return {
		"employeeOptions": employeeOptions,
	}

@frappe.whitelist() # Still needs to be tested
def get_suppliers_owned_by_supplier_employees(supplier):
	# frappe.msgprint(f"Supplier Function works. Supplier: {supplier}")
	try:
		supplier_doc = frappe.get_doc("Supplier", supplier)
	except frappe.DoesNotExistError:
		frappe.throw(_("Supplier not found"))

	employee_list = [e.employee_email for e in supplier_doc.employees]
	# frappe.msgprint(f"Employee List: {employee_list}")
	supplier_options_list = []

	for e in employee_list:
		suppliers = frappe.get_all("Supplier", filters={"owner": e}, fields=["name"], pluck="name")
		supplier_options_list.extend(suppliers)
	# frappe.msgprint(f"Supplier Option List: {supplier_options_list}")
	supplier_options = [{"label": d, "value": d} for d in supplier_options_list]
	# frappe.msgprint(f"Supplier Options: {supplier_options}")
	return {
		"supplier_options": supplier_options,
	}
