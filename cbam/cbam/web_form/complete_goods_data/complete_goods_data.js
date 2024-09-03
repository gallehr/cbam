frappe.ready(function() {
	// Corrected after_load function
	frappe.web_form.after_load = function() {
		frappe.msgprint("test");  // This should show "test" when the form loads

		// Make sure 'supplier' is a string representing the field name
		let value = frappe.web_form.get_value('supplier');
		frappe.msgprint(value); // This will show the value of the supplier field
	}

	frappe.web_form.validate = function() {
		let data = frappe.web_form.get_values();
		if (!data.is_data_confirmed) {
			frappe.msgprint('Please confirm the data by clicking the checkbox');
			return false;
		}
	};
});
