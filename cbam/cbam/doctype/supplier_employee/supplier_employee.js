// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Supplier Employee", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Supplier Employee", {
	refresh(frm) {
		frm.add_custom_button(__("Send Email"), function () {
			frappe.call({
				method: "cbam.send_email_from_employee.create_user_and_send_email", // OPEN
				args: {
					employee: cur_frm.docname,
                    supplier: cur_frm.doc.supplier_company,
				},
			});
		}, __("⚠️ Look out! ⚠️"));
	},
});
