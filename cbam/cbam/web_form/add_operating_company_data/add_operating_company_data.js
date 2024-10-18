



frappe.ready(function() {
	frappe.call({
		method: "cbam.cbam.web_form.add_operating_company_data.add_operating_company_data.get_country_codes",
		callback: (r) => {
			if (r.message.countryCodesOptions && r.message.countryCodesOptions.length > 0) {
				frappe.web_form.fields_dict["country_code"]._data = r.message.countryCodesOptions;
			}
		}
	});
	
	frappe.web_form.after_save = () => {
		console.log("OKk")
		console.log(frappe.web_form.doc.name)
		frappe.call({
			method: "cbam.cbam.web_form.add_operating_company_data.add_operating_company_data.setup_new_employee",
			args: {
				"parent_supplier":frappe.web_form.get_value("parent_supplier"),
				"email": frappe.web_form.get_value("email")
		}
	});
}
});



