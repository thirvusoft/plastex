from frappe.core.doctype.communication.communication import Communication
import frappe
from frappe.model.document import Document
import frappe
from frappe import _
import json
from frappe.core.utils import get_parent_doc
from frappe.desk.doctype.todo.todo import ToDo
from frappe.email.doctype.email_account.email_account import EmailAccount
from frappe.utils import get_formatted_email, get_url, parse_addr
from frappe.core.doctype.communication.mixins import CommunicationEmailMixin


class _CommunicationEmailMixin(CommunicationEmailMixin):
    def mail_cc(self, is_inbound_mail_communcation=False, include_sender=False):
        """Build cc list to send an email.

        * if email copy is requested by sender, then add sender to CC.
        * If this doc is created through inbound mail, then add doc owner to cc list
        * remove all the thread_notify disabled users.
        * Remove standard users from email list
        """
        if hasattr(self, "_final_cc"):
            return self._final_cc

        cc = self.cc_list()

        # Need to inform parent document owner incase communication is created through inbound mail
        if include_sender:
            cc.append(self.sender_mailid)
        if is_inbound_mail_communcation:
            if (doc_owner := self.get_owner()) not in frappe.STANDARD_USERS:
                cc.append(doc_owner)
            cc = set(cc) - {self.sender_mailid}
            cc.update(self.get_assignees())

        cc = set(cc) - set(self.filter_thread_notification_disbled_users(cc))
        cc = cc - set(self.mail_recipients(is_inbound_mail_communcation=is_inbound_mail_communcation))

        # # Incase of inbound mail, to and cc already received the mail, no need to send again.
        if is_inbound_mail_communcation:
            cc = cc - set(self.cc_list() + self.to_list())

        self._final_cc = [m for m in cc if m not in frappe.STANDARD_USERS]
        return self._final_cc
    def get_content(self, print_format=None):
        if print_format:
            return self.content + self.get_attach_link(print_format)
        return self.content
    def get_attach_link(self, print_format):
        """Returns public link for the attachment via `templates/emails/print_link.html`."""
        return '' if not isinstance(print_format, str) else frappe.get_template("templates/emails/print_link.html").render(
            {
                "url": get_url(),
                "doctype": self.reference_doctype,
                "name": self.reference_name,
                "print_format": print_format,
                "key": get_parent_doc(self).get_document_share_key(),
            }
		)
    def get_assignees(self):
        """Get owners of the reference document."""
        filters = {
            "status": "Open",
            "reference_name": self.reference_name,
            "reference_type": self.reference_doctype,
        }
        return ToDo.get_owners(filters)
    def sendmail_input_dict(
        self,
        print_html=None,
        print_format=None,
        send_me_a_copy=None,
        print_letterhead=None,
        is_inbound_mail_communcation=None,
    ) -> dict:

        outgoing_email_account = self.get_outgoing_email_account()
        if not outgoing_email_account:
            return {}

        recipients = self.get_mail_recipients_with_displayname(
            is_inbound_mail_communcation=is_inbound_mail_communcation
        )
        cc = self.get_mail_cc_with_displayname(
            is_inbound_mail_communcation=is_inbound_mail_communcation, include_sender=send_me_a_copy
        )
        bcc = self.get_mail_bcc_with_displayname(
            is_inbound_mail_communcation=is_inbound_mail_communcation
        )

        if not (recipients or cc):
            return {}

        try:
            load_attachments = json.loads(print_format)
            print_format = load_attachments
        except:
            frappe.log_error()

        final_attachments=[]
        
        if isinstance(print_format, list):
            for pf in print_format:
                self.reference_doctype=pf.get('reference_doctype')
                self.reference_name=pf.get('reference_name')
                att = self.mail_attachments(print_format=pf.get('print_format'), print_html=print_html)
                if att:
                    final_attachments.append(att[0])
        else:
            final_attachments = self.mail_attachments(print_format=print_format, print_html=print_html)
        incoming_email_account = self.get_incoming_email_account()
        return {
            "recipients": recipients,
            "cc": cc,
            "bcc": bcc,
            "expose_recipients": "header",
            "sender": self.get_mail_sender_with_displayname(),
            "reply_to": incoming_email_account and incoming_email_account.email_id,
            "subject": self.subject,
            "content": self.get_content(print_format=print_format),
            "reference_doctype": self.reference_doctype,
            "reference_name": self.reference_name,
            "attachments": final_attachments,
            "message_id": self.message_id,
            "unsubscribe_message": self.get_unsubscribe_message(),
            "delayed": True,
            "communication": self.name,
            "read_receipt": self.read_receipt,
            "is_notification": (self.sent_or_received == "Received" and True) or False,
            "print_letterhead": print_letterhead,
        }


class _Communication(Communication, _CommunicationEmailMixin):
    pass