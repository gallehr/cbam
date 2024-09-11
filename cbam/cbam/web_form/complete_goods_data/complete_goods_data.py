import frappe

def get_context(context):
	# do your magic here
	pass


@frappe.whitelist()
def get_filtered_supplier_employees(supplier):
	employeeOptions = frappe.get_all("Supplier Employee Item", {"parenttype": "Supplier", "parentfield": "employees", "parent": supplier}, ["employee_number"],distinct=1)
	employeeOptions = [{"label": d.employee_number, "value": d.employee_number} for d in employeeOptions]
	return {
		"employeeOptions": employeeOptions,
	}
