// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("Supplier", {
	refresh(frm) {
		frm.add_custom_button(__("Get Suppliers Goods"), function () {
			frappe.call({
				method: "cbam.doctype.supplier.supplier.add_linked_goods_to_childtable",
				args: {
					supplier_name: frm.doc.name,
				},
			});
		});
	},
});
