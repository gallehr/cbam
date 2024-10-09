// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('Good', {
    supplier(frm) {
        frm.set_query("employee", (doc) => {
            return {
                filters: {
                    "supplier_company": doc.supplier
                }
            }
        });
    }
})

frappe.ui.form.on('Good', {
    installation(frm) {
        frm.set_query("emission_data", (doc) => {
            return {
                filters: {
                    "cbam_installation": doc.installation
                }
            }
        });
    }
})

frappe.ui.form.on("Good", {
    refresh(frm) {
        frm.add_custom_button(__("Send Email"), function () {
            // console.log("create new supplier");
            frappe.call({
                method: "cbam.send_email_from_good.send_email",
                args: {
                    good: cur_frm.docname,
                },
            });
        }, __("⚠️ Look out! ⚠️"));
    },
});