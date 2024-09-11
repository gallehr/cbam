frappe.ready(function() {
	frappe.web_form.validate = function() {
		let data = frappe.web_form.get_values();
		if (!data.is_data_confirmed) {
			frappe.msgprint('Please confirm the data by clicking the checkbox');
			return;
		}
	};

	frappe.web_form.on("responsibility_1", function() {
		let supplier = frappe.web_form.get_value('supplier');
		if (supplier) {
			frappe.call({
				method: "cbam.cbam.web_form.complete_goods_data.complete_goods_data.get_filtered_supplier_employees",
				args: {supplier},
				callback: (r) => {
					if (r.message.employeeOptions && r.message.employeeOptions.length > 0) {
						frappe.web_form.fields_dict["responsible_employee_1"]._data = r.message.employeeOptions;
					}
				}
			});
		}
	});
});