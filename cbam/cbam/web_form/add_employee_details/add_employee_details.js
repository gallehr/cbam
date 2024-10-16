frappe.ready(function() {
    frappe.call({
        method: "cbam.get_supplier_number.get_supplier_number.get_supplier_number",
        callback: function (response) {
            if (response.message) {
                if (response.message) {
                    frappe.web_form.set_value("supplier_company", response.message);
                }
            }
        }
    });
});