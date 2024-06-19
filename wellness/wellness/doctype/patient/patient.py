# Copyright (c) 2024, Wellness tech and contributors
# For license information, please see license.txt

# import frappe
#from frappe.model.document import Document
# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt


import dateutil

import frappe
from frappe import _
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.contacts.doctype.contact.contact import get_default_contact
from frappe.model.document import Document



class Patient(Document):

	def validate(self):
		self.set_full_name()
		self.flags.is_new_doc = self.is_new()
	

	def set_full_name(self):
		if self.last_name:
			self.patient_name = " ".join(filter(None, [self.first_name, self.last_name]))
		else:
			self.patient_name = self.first_name


	def create_website_user(self):
		users = frappe.db.get_all(
			"User",
			fields=["email", "mobile_no"],
			or_filters={"email": self.email, "mobile_no": self.mobile},
		)
		if users and users[0]:
			frappe.throw(
				_(
					"User exists with Email {}, Mobile {}<br>Please check email / mobile or disable 'Invite as User' to skip creating User"
				).format(frappe.bold(users[0].email), frappe.bold(users[0].mobile_no)),
				frappe.DuplicateEntryError,
			)

		user = frappe.get_doc(
			{
				"doctype": "User",
				"first_name": self.first_name,
				"last_name": self.last_name,
				"email": self.email,
				"user_type": "Website User",
				"mobile_no": self.mobile,
				"birth_date": self.dob,
			}
		)
		user.flags.ignore_permissions = True
		user.enabled = True
		user.send_welcome_email = True
		user.add_roles("Patient")
		self.db_set("user_id", user.name)

	
