import frappe

@frappe.whitelist()
def get_supplier_number():
    session_user = frappe.session.user
    supplier_number = frappe.db.get_all("Supplier Employee", filters={"email": session_user}, fields=["supplier_company"], pluck="supplier_company")
    if (len(supplier_number) == 0):
        frappe.throw("Could not find supplier number for your user: " + session_user)
    elif (len(supplier_number) > 1):
        frappe.throw("Found multiple supplier numbers for your user: " + session_user)
    else:
        return supplier_number