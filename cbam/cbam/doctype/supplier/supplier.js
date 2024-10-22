// Copyright (c) 2024, phamos GmbH and contributors
// For license information, please see license.txt


frappe.ui.form.on('Supplier', {
	refresh(frm) {
		if(frappe.user.has_role("System Manager")){
			frm.add_custom_button(__("Delete All Employees"), function(){
				frappe.warn( 
					__('Are you sure you want to proceed?'),
					__('This will delete all the linked employees.'),
					() => {
						frappe.call({
							method: "delete_linked_employees",
							doc: frm.doc,
							freeze: true,
							freeze_message: "Deleting Linked Empoyees, please wait ....",
							callback(r){
								if(r.message){
									frm.reload_doc()
									msgprint(r.message)
								}
							}
						});
					}, () => {
				})
			})
		}
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