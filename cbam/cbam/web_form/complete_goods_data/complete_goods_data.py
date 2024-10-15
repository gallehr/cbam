import frappe

def get_context(context):
	# do your magic here
	pass


@frappe.whitelist()
def get_filtered_supplier_employees(supplier, employee):
	#frappe.msgprint(f"Employee Function works. Supplier: {supplier}, Employee: {employee}")
	# employeeOptions = frappe.get_all("Supplier Employee Item", {"parenttype": "Supplier", "parentfield": "employees", "parent": supplier}, ["employee_number"], distinct=1)
	supplier_doc = frappe.get_doc("Supplier", supplier)
	employee_option_list = [e.employee_number for e in supplier_doc.employees]
	#frappe.msgprint(f"Employee Options: {employeeOptions}")
	employeeOptions = [{"label": d, "value": d} for d in employee_option_list if d != employee]
	#frappe.msgprint(f"Employee Options: {str(employeeOptions)}")
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

@frappe.whitelist()
def check_if_supplier_user():
    user_email = frappe.session.user
    # frappe.msgprint(str(user_email))
    try:
        user = frappe.get_doc("User", user_email)
    except frappe.DoesNotExistError:
        frappe.throw(_("User not found"))
    role_list = [r.role for r in user.roles]
    # frappe.msgprint(str(role_list))
    if "Supplier" in role_list:
        employee_list = frappe.get_all("Supplier Employee", filters={"email": user_email}, fields=["name"], pluck="name")
        if not employee_list:
            frappe.throw("You are not registered as an employee of a supplier. Please login with another user.")
            return False
        elif len(employee_list) > 1:
            frappe.throw("You are registered as an employee of more than one supplier. Please contact the system administrator.")
            return False
        else:
            return True, employee_list
    else:
        frappe.throw("You are not registered as a supplier. A valid selection for the Field 'Installation Name' couldn't be created.")


@frappe.whitelist()
def get_filtered_emission_data():
    try:
        is_supplier_user, employee_list = check_if_supplier_user()
        if is_supplier_user:
            supplier = frappe.db.get_value("Supplier Employee", employee_list[0], "supplier_company")
            operating_company_list = frappe.db.get_all("CBAM Operating Company", filters={"parent_supplier": supplier}, fields=["name"], pluck="name")
            #frappe.msgprint(f"Operating Company List: {operating_company_list}")
            if len(operating_company_list) == 1:
                emission_data_list = frappe.get_all("CBAM Emission Data", filters={"operator_name": operating_company_list[0]}, fields=["name", "installation_name"])
                #frappe.msgprint(f"Emission Data List: {emission_data_list}")
                emission_data_options = [{"label": e.name, "value": e.installation_name} for e in emission_data_list]
                #frappe.msgprint(f"Emission Data Options: {emission_data_options}")
            elif len(operating_company_list) < 1:
                #frappe.throw("Couldn't find any Operating Company for your Supplier.")
                return {
					"emissionDataOptions": [],
				}
            else:
                frappe.throw("Found more than one Operating Company for your Supplier. Please contact the system administrator.")

            #frappe.msgprint(str(installation_options))
            #installation_options = [{"label": i.name_of_the__installation, "value": i.name} for i in installation_option_list]
            return {
                "emissionDataOptions": emission_data_options,
            }
    except:
        frappe.throw("Couldn't create a valid selection for the Field 'Emission Data'.")

@frappe.whitelist()
def is_operating_company_registered():
    try:
        is_supplier_user, employee_list = check_if_supplier_user()
        if is_supplier_user:
            supplier = frappe.db.get_value("Supplier Employee", employee_list[0], "supplier_company")
            operating_company_list = frappe.db.get_all("CBAM Operating Company", filters={"parent_supplier": supplier}, fields=["name"], pluck="name")
            #frappe.msgprint(f"Operating Company List: {operating_company_list}")
            if len(operating_company_list) > 0:
            	return {
					"isOperatingCompanyRegistered": 1,
				}
            else:
            	return {
					"isOperatingCompanyRegistered": 0,
				}
    except:
        frappe.throw("Error: Couldn't check if the Operating Company is registered.")
