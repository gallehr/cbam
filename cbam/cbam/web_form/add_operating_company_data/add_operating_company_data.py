import frappe

def get_context(context):
	# do your magic here
	pass

@frappe.whitelist()
def get_country_codes():
    try:
        country_code_list = frappe.get_all("Country Code", fields=["name", "country_full_name"])
        country_code_options = [{"label": c.country_full_name, "value": c.name} for c in country_code_list]
        return {
            "countryCodesOptions": country_code_options,
        }
    except:
        frappe.throw("Couldn't create a valid selection for the Field 'Country'.")