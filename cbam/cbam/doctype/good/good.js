// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

// Not working
frappe.ui.form.on('Good', {
 refresh(frm) {
     frm.set_query("employee", (doc) => {
         return {
             filters: {
                 "supplier_company": doc.supplier
             }
         }
     });
 }
})
