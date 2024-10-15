// console.log("add_employee_details.js loaded");
frappe.ready(function() {
    frappe.call({
        method: "cbam.get_supplier_number",
        callback: function (response) {
            // console.log(`{frappe.session.user="${frappe.session.user}"}`)
            // console.log(`{response="${response}"}`)
            if (response.message) {
                // console.log(`{response.message="${response.message}"}`)
                if (response.message) {
                    frappe.web_form.set_value("supplier_company", response.message);
                }
            }
        }
    });
});