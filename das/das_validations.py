import frappe
from datetime import datetime as dt

def delivery_note_validations(doc, method):
	# start date end end date
	start = dt.strptime(doc.start_date, "%Y-%m-%d %H:%M:%S")
	end  = dt.strptime(doc.end_date, "%Y-%m-%d %H:%M:%S")

	tech_details = is_technician_timeslot_free(start, end, doc.technician)

	if tech_details:
		frappe.throw("%s is already assigned for other delivery note between given Start Date & End Date"%(doc.technician))
	if start > end:
		frappe.throw("End Date should be greater than Start Date")
	elif start == end:
		frappe.throw("End Date can not be same as Start Date")

def is_technician_timeslot_free(_from, _to, technician):
	return frappe.db.sql("""SELECT name FROM `tabDelivery Note` WHERE technician='%s' AND docstatus<>2 AND 
		(start_date between '%s' AND '%s' OR end_date between '%s' AND '%s')"""%(technician,_from,_to,_from,_to),
		as_dict=True, debug=1)

def validations_against_batch_number(doc, method):
	err_items = []
	for item in doc.items:
		if frappe.db.get_value("Item",item.item_code,"has_batch_no") == "Yes" and not item.batch_no:
			err_items.append(item.item_code)

	if err_items:
		frappe.throw("Item Batch Number is mandatory for item(s) {err_items}".format(err_items = ",".join(err_items)))
