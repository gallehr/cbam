import frappe
from frappe.model.document import Document

# for testing in console
# parent_good = "GOO-MRN1000"

@frappe.whitelist()
def split_good(parent_good, percentage1, percentage2, percentage3, percentage4, percentage5):
    # check if parent_good was already splitted once before
    mrn_split_serie = frappe.get_all("Good", filters={
        "name": ["like", parent_good + "-" + "%"]
    }, pluck="name")
    if mrn_split_serie:
        split_number_list = []
        for mrn in mrn_split_serie:
            splitted_mrn = mrn.split("-")
            last_split_number = int(splitted_mrn[-1])
            split_number_list.append(last_split_number)
            # split_number_list = [int(mrn.split(".")[-1]) for mrn in mrn_split_serie]
            next_highest_split_number = max(split_number_list) + 1
        # next_highest_split_number_str=str(next_highest_split_number)
        # if len(next_highest_split_number_str) == 1:
        #     next_highest_split_number_str = "0" + next_highest_split_number_str
    else:
        next_highest_split_number = 0

    # insert a new good in database
    doc = frappe.get_doc("Good", parent_good)
    if percentage1 and percentage1 != "0":
        new_good = frappe.new_doc("Good")
        new_good.master_reference_number_mrn = doc.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
        new_good.good_description = doc.good_description
        new_good.customs_tariff_number = doc.customs_tariff_number
        new_good.hand_over_date = doc.hand_over_date
        new_good.supplier = doc.supplier
        new_good.raw_mass = doc.raw_mass / 100 * int(percentage1)
        new_good.insert()
        next_highest_split_number += 1
    if percentage2 and percentage2 != "0":
        new_good = frappe.new_doc("Good")
        new_good.master_reference_number_mrn = doc.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
        new_good.good_description = doc.good_description
        new_good.customs_tariff_number = doc.customs_tariff_number
        new_good.hand_over_date = doc.hand_over_date
        new_good.supplier = doc.supplier
        new_good.raw_mass = doc.raw_mass / 100 * int(percentage2)
        new_good.insert()
        next_highest_split_number += 1
    if percentage3 and percentage3 != "0":
        new_good = frappe.new_doc("Good")
        new_good.master_reference_number_mrn = doc.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
        new_good.good_description = doc.good_description
        new_good.customs_tariff_number = doc.customs_tariff_number
        new_good.hand_over_date = doc.hand_over_date
        new_good.supplier = doc.supplier
        new_good.raw_mass = doc.raw_mass / 100 * int(percentage3)
        new_good.insert()
        next_highest_split_number += 1
    if percentage4 and percentage4 != "0":
        new_good = frappe.new_doc("Good")
        new_good.master_reference_number_mrn = doc.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
        new_good.good_description = doc.good_description
        new_good.customs_tariff_number = doc.customs_tariff_number
        new_good.hand_over_date = doc.hand_over_date
        new_good.supplier = doc.supplier
        new_good.raw_mass = doc.raw_mass / 100 * int(percentage4)
        new_good.insert()
        next_highest_split_number += 1
    if percentage5 and percentage5 != "0":
        frappe.msgprint(percentage5)
        new_good = frappe.new_doc("Good")
        new_good.master_reference_number_mrn = doc.master_reference_number_mrn + "-" + f"{next_highest_split_number:02}"
        new_good.good_description = doc.good_description
        new_good.customs_tariff_number = doc.customs_tariff_number
        new_good.hand_over_date = doc.hand_over_date
        new_good.supplier = doc.supplier
        new_good.raw_mass = doc.raw_mass / 100 * int(percentage5)
        new_good.insert()