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
from frappe.email.email_body import get_message_id
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
from frappe.email.queue import send_one


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
'''
@frappe.whitelist()
def send_mail(values,docname,content):
	communication_medium="Email"
	sent_or_received = "Sent"
	from email.utils import formataddr
	print_settings = frappe.get_doc("Print Settings", "Print Settings")
	email_template = ""
	content = ""
	cc = ""
	bcc = ""
	values = json.loads(values)
	if "email_template" in values:
		email_template = values['email_template']
	#if 'content' in values:
	#	content = values['content']
	print "content-----------",content
	to = ""
	
	
	
	lang_1 = values['select_language']
	lang_2 = values['select_languages']
	cc_email = ""
	
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
	
	if values["attach_document_print"] == 0:
		attachments = ""
	elif values["attach_document_print"] == 1:
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
	recipient_re = []
	recipient_list= {}
	if 'recipients' in values:
		to = values['recipients']
		print "to0-----------",to
		for i in to:
			i =  i.strip()
			
			recipient_re.append(str(i))
			
	
	cc_mails_re = []
	cc_list = ""
	cc = ""
	if 'cc' in values:
		cc = values['cc']
		for i in cc:
			i =  i.strip()
			cc_mails_re.append(str(i))
		cc_list = list(filter(None, cc_mails_re))	

	bcc_emails_re = []
	bcc_list = ""
	bcc = ""
	if 'bcc' in values:
		bcc = values['bcc']
		for i in bcc_emails:
			i =  i.strip()
			bcc_emails_re.append(str(i))
		bcc_list = list(filter(None, bcc_emails_re))
	
	#for rep in recipient:
	#	rep = rep.strip()
	#	if rep != ' ' and rep != "" and rep != None:
	#		 recipient_re.append(rep)
	
	#for rep in cc_mails:
	#	if rep != ' ' and rep != "" and rep != None:
	#		 cc_mails_re.append(rep)
	#bcc_emails_re = []
	#for rep in bcc_emails:
	#	if rep != ' ' and rep != "" and rep != None:
	#		 bcc_emails_re.append(rep)
	
	frappe.sendmail(recipients = recipient_list,
			subject = values['subject'],
			sender = sender[0]['email_id'],
			cc = cc_list,
			bcc = bcc_list,
			#message = frappe.render_template(self.message, context),
			message = content,
			reference_doctype = "Purchase Order",
			reference_name = docname,
			attachments = attachments,
			print_letterhead = ((attachments
				and attachments[0].get('print_letterhead')) or False))
	
	doctype = "Purchase Order"
	read_receipt=None
	send_me_a_copy=False
	print_format=None
	print_html=None
	sender_full_name=None
	send_email=1
	comm = frappe.get_doc({
		"doctype":"Communication",
		"subject": values['subject'],
		"content": content,
		"sender": sender[0]['email_id'],
		"sender_full_name":sender_full_name,
		"recipients": values['recipients'],
		"cc": cc or None,
		"bcc": bcc or None,
		"communication_medium": communication_medium,
		"sent_or_received": sent_or_received,
		"reference_doctype": "Purchase Order",
		"reference_name": docname,
		"message_id":get_message_id().strip(" <>"),
		"read_receipt":read_receipt,
		"has_attachment": 1 if attachments else 0
	})
	comm.insert(ignore_permissions=True)

	if not doctype:
		# if no reference given, then send it against the communication
		comm.db_set(dict(reference_doctype='Communication', reference_name=comm.name))

	

	# if not committed, delayed task doesn't find the communication
	if attachments:
		add_attachments("Communication", comm.name, attachments)

	frappe.db.commit()
	print_letterhead=True
	if cint(send_email):
		frappe.flags.print_letterhead = cint(print_letterhead)
		comm.send(print_html, print_format, attachments, send_me_a_copy=send_me_a_copy)

	return {
		"name": comm.name,
		"emails_not_sent_to": ", ".join(comm.emails_not_sent_to) if hasattr(comm, "emails_not_sent_to") else None
	}
	#return True
'''
@frappe.whitelist()
def get_template(value):
	template = frappe.get_value("Email Template", value , 'response')
	return template
@frappe.whitelist()
def get_email_template(value):
	template = frappe.get_list("Email Template", filters={"name":value} , fields=[ 'response','subject'])
	return template

@frappe.whitelist()
def get_print_settings():
	print_settings = frappe.get_doc("Print Settings", "Print Settings")
	return print_settings
@frappe.whitelist()
def send_now(value):
	value = json.loads(value)	
	frappe.db.set_value("Communication",value['name'], "sent_via_send_mail", 1 )

@frappe.whitelist()
def send():
	#f= open("/home/frappe/frappe-bench/apps/plastex/plastex/output.out","a+")
	email_queue = frappe.get_list("Email Queue", filters={"reference_doctype": "Purchase Order", "status":"Not Sent"}, fields=["name", "communication"])
	for email in email_queue:
		comm = frappe.get_value("Communication",email['communication'], "sent_via_send_mail")
		#f.write("comm----------------"+str(comm)+'\n')
		if comm ==1:
			#f.write("name----------------"+str(email['name'])+'\n')
			send_one(email['name'], now=True)
