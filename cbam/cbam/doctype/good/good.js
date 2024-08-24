// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("Good", {
	refresh(frm) {
		frm.add_custom_button(__("Split Good"), function () {
			frappe.call({
				method: "cbam.api.split_good",
				args: {
					parent_good: frm.doc.name,
					percentage1: frm.doc.split_percentage_1,
					percentage2: frm.doc.split_percentage_2,
					percentage3: frm.doc.split_percentage_3,
					percentage4: frm.doc.split_percentage_4,
					percentage5: frm.doc.split_percentage_5,
				},
			});
		});
	},
});
