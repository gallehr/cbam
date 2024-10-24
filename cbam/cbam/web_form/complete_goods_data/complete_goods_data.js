frappe.ready(function() {
	// Employee Link Field Filter
	frappe.web_form.on("manufacture", function() {
		let supplier = frappe.web_form.get_value('supplier');
		let employee = frappe.web_form.get_value('employee');
		if (supplier) {
			frappe.call({
				method: "cbam.cbam.web_form.complete_goods_data.complete_goods_data.get_filtered_supplier_employees",
				args: {
					supplier: supplier, 
					employee:employee
				},
				callback: (r) => {
					// debugger;
					if (r.message.employeeOptions && r.message.employeeOptions.length > 0) {
						frappe.web_form.fields_dict["responsible_employee_1"]._data = r.message.employeeOptions;
						frappe.web_form.fields_dict["responsible_employee_2"]._data = r.message.employeeOptions;
						frappe.web_form.fields_dict["responsible_employee_3"]._data = r.message.employeeOptions;
						frappe.web_form.fields_dict["responsible_employee_4"]._data = r.message.employeeOptions;
						frappe.web_form.fields_dict["responsible_employee_5"]._data = r.message.employeeOptions;
					}
				}
			});
			
			if (supplier) {
				frappe.call({
					method: "cbam.cbam.web_form.complete_goods_data.complete_goods_data.get_suppliers_owned_by_supplier_employees",
					args: {
						supplier: supplier
					},
					callback: (r) => {
						//debugger;
						console.log(r.message)
						if (r.message.supplier_options && r.message.supplier_options.length > 0) {
							
							frappe.web_form.fields_dict["responsible_supplier_1"]._data = r.message.employeeOptions;
							frappe.web_form.fields_dict["responsible_supplier_2"]._data = r.message.employeeOptions;
							frappe.web_form.fields_dict["responsible_supplier_3"]._data = r.message.employeeOptions;
							frappe.web_form.fields_dict["responsible_supplier_4"]._data = r.message.employeeOptions;
							frappe.web_form.fields_dict["responsible_supplier_5"]._data = r.message.employeeOptions;
						}
					}
				});
			}
		}
	});

	// Supplier Link Field Filter


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
			} else {
				frappe.web_form.set_df_property("add_installations_and_emission_data_section", "hidden", 1);
			}
		}
	});
});