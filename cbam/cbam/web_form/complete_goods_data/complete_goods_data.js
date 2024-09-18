frappe.ready(function() {
	// Employee Link Field Filter
	frappe.web_form.on("good_values", function() {
		let supplier = frappe.web_form.get_value('supplier');
		let employee = frappe.web_form.get_value('employee');
		if (supplier) {
			frappe.call({
				method: "cbam.cbam.web_form.complete_goods_data.complete_goods_data.get_filtered_supplier_employees",
				args: {supplier, employee},
				callback: (r) => {
					// debugger;
					if (r.message.employeeOptions && r.message.employeeOptions.length > 0) {
						frappe.web_form.fields_dict["responsible_employee_1"]._data = r.message.employeeOptions;
					}
				}
			});
		}
	});

	// Supplier Link Field Filter
	frappe.web_form.on("responsibility_1", function() {
		let supplier = frappe.web_form.get_value('supplier');
		if (supplier) {
			frappe.call({
				method: "cbam.cbam.web_form.complete_goods_data.complete_goods_data.get_suppliers_owned_by_supplier_employees",
				args: {supplier},
				callback: (r) => {
					//debugger;
					frappe.msgprint(r)
					if (r.message.employeeOptions && r.message.employeeOptions.length > 0) {
						frappe.msgprint('Suppliers owned by the selected employee: ');
						frappe.web_form.fields_dict["responsible_employee_1"]._data = r.message.employeeOptions;
					}
				}
			});
		}
	});

	// // Confirmation Check box validation
	// frappe.web_form.validate = function() {
	// 	let data = frappe.web_form.get_values();
	// 	if (!data.is_data_confirmed) {
	// 		frappe.msgprint('Please confirm the data by clicking the checkbox');
	// 		return false;
	// 	}
	// };
});