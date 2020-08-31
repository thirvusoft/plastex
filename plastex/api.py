from __future__ import unicode_literals
import frappe
from frappe import _, throw, msgprint, utils
from frappe.utils import cint, flt, cstr, comma_or, getdate, add_days, getdate, rounded, date_diff, money_in_words
from frappe.model.mapper import get_mapped_doc
from frappe.model.naming import make_autoname
from erpnext.utilities.transaction_base import TransactionBase
from erpnext.accounts.party import get_party_account_currency
from frappe.desk.notifications import clear_doctype_notifications
from datetime import datetime
import sys
import os
import operator
import frappe
import json
import time
import math
import base64
import ast
import schedule

@frappe.whitelist()
def get_email_list():
	data = []
	email_list = frappe.db.sql("""select email_id from `tabEmail Account` """,as_dict=1)
	for em  in email_list:
		data.append(em.email_id)
	return data
@frappe.whitelist()
def get_print_format(doctype):
	print_list = []
	print_format = frappe.db.sql("""select name from `tabPrint Format` where doc_type = %s""",doctype,as_dict=1)
	for pr in print_format:
		print_list.append(pr.name)
	return print_list
@frappe.whitelist()
def send_mail(values,docname):
	from email.utils import formataddr
	print_settings = frappe.get_doc("Print Settings", "Print Settings")
	email_template = ""
	content = ""
	cc = ""
	bcc = ""
	values = json.loads(values)
	if "email_template" in values:
		email_template = values['email_template']
	if 'content' in values:
		content = values['content']
	to = ""
	recipients = ""
	recipient = []
	if 'recipients' in values:
		to = values['recipients']
		recipients = to.split(",")
		#print "recipients-------------",recipients
		for re in recipients:
			#print "rev-----------------",re
			if re != "":
				recipient.append(re)
		#print "recipient-------------",recipient
	
	lang_1 = values['select_language']
	lang_2 = values['select_languages']
	cc_email = ""
	cc_mails = []
	if 'cc' in values:
		cc = values['cc']
		cc_email = cc.split(",")
		#print "cc_email-------------",cc_email
		for cc in cc_email:
			if cc != "":
				cc_mails.append(cc)
		#print "cc_mails-------------",cc_mails
			
	bcc_email = ""
	bcc_emails = []
	if 'bcc' in values:
		bcc = values['bcc']
		bcc_email = bcc.split(",")
		#print "bcc_email-------------",bcc_email
		for bcc in bcc_email:
			if bcc != "":
				bcc_emails.append(bcc)
		#print "bcc_emails-------------",bcc_emails
	print_format1 = ""
	if 'select_print_format' in values:
		
		print_format1 = values['select_print_format']
	print_format2 = ""
	if 'select_print_formats' in values:
		print_format2 = values['select_print_formats']
	purchase_order = 'Purchase Order'
	sales_order = values['sales_order']
	#template = ""
	if 'email_template' in values:
		content =  get_template(values['email_template'])
	attachments = ""
	if 'select_print_format' in values and 'select_print_formats' in values:
		attachments = [{
					"print_format_attachment": 1,
					"doctype": purchase_order,
					"name": docname,
					"print_format": print_format1,
					"print_letterhead": print_settings.with_letterhead,
					"lang": lang_1
				},
				{
					"print_format_attachment": 1,
					"doctype": 'Sales Order',
					"name": sales_order,
					"print_format": print_format2,
					"print_letterhead": print_settings.with_letterhead,
					"lang": lang_2
				}
				]
	else:
		frappe.throw("Please select first print formats")
	sender = frappe.get_list('Email Account', filters={"default_outgoing":1}, fields=['email_id'])
	frappe.sendmail(recipients = recipient,
			subject = values['subject'],
			sender = sender[0]['email_id'],
			cc = cc_mails,
			bcc = bcc_emails,
			#message = frappe.render_template(self.message, context),
			message = content,
			reference_doctype = "Purchase Order",
			reference_name = docname,
			attachments = attachments,
			print_letterhead = ((attachments
				and attachments[0].get('print_letterhead')) or False))
	return True
@frappe.whitelist()
def get_template(value):
	template = frappe.get_value("Email Template", value , 'response')
	return template

@frappe.whitelist()
def get_email_template(value):
	template = frappe.get_list("Email Template", filters={"name":value} , fields=[ 'response','subject'])
	return template

