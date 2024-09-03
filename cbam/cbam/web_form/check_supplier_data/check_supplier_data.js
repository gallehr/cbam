// frappe.ready(function() {
// 	// bind events here
// })

frappe.web_form.after_load = () => {
	frappe.msgprint("Please fill all values carefully");
};

frappe.web_form.validate = () => {
	let data = frappe.web_form.get_values();
	if (!data.is_data_confirmed) {
		// If checkbox is not checked
		frappe.msgprint("Please check the confirmation checkbox");
		return false;
	}
};
