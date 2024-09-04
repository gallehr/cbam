frappe.ready(function() {
	frappe.web_form.after_load = (e) => {
        frappe.msgprint('Please fill all values carefully');
        console.log(e)
    }
});