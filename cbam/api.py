import frappe
from frappe.model.document import Document

# for testing in console
# parent_good = "GOO-MRN1000"

@frappe.whitelist()
def split_good(parent_good, percentage):
    # check if parent_good was already splitted once before
    mrn_split_serie = frappe.get_all("Good", filters={
        "name": ["like", parent_good + "#" + "%"]
    }, pluck="name")
    if mrn_split_serie:
        # get highest split number and add 1
        # mrn_split_serie = frappe.get_all("Good", filters={
        #     "name": ["like", parent_good + "%"]
        # }, pluck="name")
        split_number_list = []
        for mrn in mrn_split_serie:
            splitted_mrn = mrn.split("#")
            last_split_number = int(splitted_mrn[-1])
            split_number_list.append(last_split_number)
            # split_number_list = [int(mrn.split(".")[-1]) for mrn in mrn_split_serie]
            next_highest_split_number = max(split_number_list) + 1
        next_highest_split_number_str=str(next_highest_split_number)
        if len(next_highest_split_number_str) == 1:
            next_highest_split_number_str = "0" + next_highest_split_number_str
    else:
        next_highest_split_number_str = "00"

    # insert a new good in database
    doc = frappe.get_doc("Good", parent_good)
    new_good = frappe.new_doc("Good")
    new_good.master_reference_number_mrn = doc.master_reference_number_mrn + "#" + next_highest_split_number_str
    new_good.good_description = doc.good_description
    new_good.customs_tariff_number = doc.customs_tariff_number
    new_good.hand_over_date = doc.hand_over_date
    new_good.supplier = doc.supplier
    new_good.raw_mass = doc.raw_mass / 100 * int(percentage)
    new_good.insert()