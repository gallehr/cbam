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

	frappe.call({
		method: "cbam.cbam.web_form.complete_goods_data.complete_goods_data.get_filtered_emission_data",
		callback: (r) => {
			if (r.message.emissionDataOptions && r.message.emissionDataOptions.length > 0) {
				frappe.web_form.fields_dict["emission_data"]._data = r.message.emissionDataOptions;
			}
		}
	});

	// Hide Operating Company Section if Operating Company is Registered
	frappe.call({
		method: "cbam.cbam.web_form.complete_goods_data.complete_goods_data.is_operating_company_registered",
		callback: (r) => {
			if (r.message.isOperatingCompanyRegistered && r.message.isOperatingCompanyRegistered == 1) {
				frappe.web_form.set_df_property("add_operating_company_section", "hidden", 1);
			}
		}
	});
});