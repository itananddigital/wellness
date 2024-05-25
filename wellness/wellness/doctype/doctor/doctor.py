# Copyright (c) 2024, Wellness tech and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


@frappe.whitelist(allow_guest=True)
def get_doctor_details(doctor_name):
    doctor = frappe.get_doc("Doctor", doctor_name)
    return {
        "profile": doctor.profile,
        "first_name": doctor.first_name,
        "last_name": doctor.last_name,
        "specialization": doctor.specialization,
        "city": doctor.city,
        "status": doctor.status,
		"booking_slots": doctor.booking_slots,
    }

class Doctor(WebsiteGenerator):
	pass
