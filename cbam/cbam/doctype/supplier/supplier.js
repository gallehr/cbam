// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Supplier", {
// 	refresh(frm) {
// 		frm.add_custom_button(__("Get Suppliers Goods"), function () {
// 			frappe.call({
// 				method: "cbam.doctype.supplier.supplier.add_linked_goods_to_childtable",
// 				args: {
// 					supplier_name: frm.doc.name,
// 				},
// 			});
// 		});
// 	},
// });

// frappe.ui.form.on("Supplier", {
// 	// whenever "state" field is changed
// 	refresh(frm) {
// 		frm.set_query("supplier_employees", (doc) => {
// 			return {
// 				filters: {
// 					"employee_number": doc.name, // whatever state is selected
// 				},
// 			};
// 		});
// 	},
// });

frappe.ui.form.on('Supplier', {
	refresh(frm) {
		// your code here
	}
})

frappe.ui.form.on('Supplier Employee Item', {
	refresh(frm) {
		frm.set_query("employee_number", (doc) => {
			return {
				filters: {
					"supplier_company": "00000001",
				},
			};
		});
	},
});

//  https://discuss.frappe.io/t/filter-child-table/86467 or https://discuss.frappe.io/t/filter-link-field-on-child-table/75184 
function filterChildFields(frm, tableName, fieldTrigger, fieldName, fieldFiltered) {
    frm.fields_dict[tableName].grid.get_field(fieldFiltered).get_query = function(doc, cdt, cdn) {
        var child = locals[cdt][cdn];
        return {
            filters:[
                [fieldName, '=', child[fieldTrigger]]
            ]
        }
    }
}