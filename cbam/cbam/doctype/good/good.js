// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

// // Not working
// frappe.ui.form.on('Good', {
//  refresh(frm) {
//      frm.set_query("employee", (doc) => {
//          return {
//              filters: {
//                  "supplier_company": doc.supplier
//              }
//          }
//      });
//  }
// })

frappe.ui.form.on("Good", {
	sent_to_supplier_employee(frm) {
			frappe.call({
				method: "cbam.detail_confirmation_email.send_email",
				args: {
					supplier: cur_frm.doc.supplier,
                    employee: cur_frm.doc.employee
				},
			});
	},
});
