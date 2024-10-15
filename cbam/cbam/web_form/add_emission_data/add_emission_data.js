frappe.ready(function() {
	frappe.call({
		method: "cbam.cbam.web_form.add_emission_data.add_emission_data.get_filtered_installations",
		callback: (r) => {
			if (r.message.installationOptions && r.message.installationOptions.length > 0) {
				frappe.web_form.fields_dict["cbam_installation"]._data = r.message.installationOptions;
			}
		}
	});
});