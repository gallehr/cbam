frappe.ready(function() {
	frappe.call({
		method: "cbam.cbam.web_form.add_installation_data.add_installation_data.get_country_codes",
		callback: (r) => {
			if (r.message.countryCodesOptions && r.message.countryCodesOptions.length > 0) {
				frappe.web_form.fields_dict["country_code"]._data = r.message.countryCodesOptions;
			}
		}
	});
});