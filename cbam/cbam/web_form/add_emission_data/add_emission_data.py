import frappe

def get_context(context):
	# do your magic here
	pass

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
def get_filtered_installations():
    try:
        is_supplier_user, employee_list = check_if_supplier_user()
        if is_supplier_user:
            supplier = frappe.db.get_value("Supplier Employee", employee_list[0], "supplier_company")
            operating_company_list = frappe.db.get_all("CBAM Operating Company", filters={"parent_supplier": supplier}, fields=["name"], pluck="name")
            if len(operating_company_list) == 1:
                operating_company_doc = frappe.get_doc("CBAM Operating Company", operating_company_list[0])
            else:
                frappe.throw("Couldn't any or more than one Operating Company for your Supplier.")
            installation_options = [{"label": i.installation_name, "value": i.cbam_installation} for i in operating_company_doc.installations]
            #frappe.msgprint(str(installation_options))
            #installation_options = [{"label": i.name_of_the__installation, "value": i.name} for i in installation_option_list]
            return {
                "installationOptions": installation_options,
            }
    except:
        frappe.throw("Couldn't create a valid selection for the Field 'Installation Name'.")
