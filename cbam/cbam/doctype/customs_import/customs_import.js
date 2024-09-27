// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Customs Import", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Customs Import", {
	refresh(frm) {
		frm.add_custom_button(__("Sent all Emails (yet not sent)"), function () {
			frappe.call({
				method: "cbam.send_email_from_customs_import.create_user_and_send_email", // OPEN
				args: {
					goods_list: cur_frm.doc.goods,
				},
			});
		}, __("⚠️ Look out! ⚠️"));
	},
});
