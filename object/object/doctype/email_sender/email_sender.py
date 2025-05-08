# Copyright (c) 2025, nextash and contributors
# For license information, please see license.txt

import frappe
from bs4 import BeautifulSoup
from frappe.utils import cstr
from frappe import _
from frappe.model.document import Document


class EmailSender(Document):
    def get_timeline_data(self, parent_doctype, parent_name):
        return {
            "reference_doctype": self.reference_doctype,
            "reference_name": self.reference_name
        }

@frappe.whitelist()
def send_email_and_save(data):
    data = frappe._dict(data)

    # Send Email
    frappe.sendmail(
        recipients=[data.recipient],
        subject=data.subject,
        message=data.message,
    )

    # Save record
    doc = frappe.new_doc('Email Sender')
    doc.recipient = data.recipient
    doc.subject = data.subject
    doc.message = data.message
    doc.insert(ignore_permissions=True)

    return {'status': 'success'}
@frappe.whitelist()
def reply(email_sender_name, subject, message):
    original = frappe.get_doc('Email Sender', email_sender_name)

    frappe.sendmail(
        recipients=[original.recipient],
        subject=subject,
        message=message,
        now=True
    )

    doc = frappe.new_doc('Email Sender')
    doc.recipient = original.recipient
    doc.subject = subject
    doc.message = message
    doc.insert(ignore_permissions=True)

    return {'status': 'replied'}


@frappe.whitelist()
def relink_and_send_email(reference_doctype, reference_name, docname):
    eamaail_doc = frappe.get_doc('Email Sender', docname)

    doc=frappe.get_doc({"doctype": "Communication","communication_type": "Communication","subject": eamaail_doc.subject,"content": eamaail_doc.message,"sent_or_received": "Sent","reference_doctype": reference_doctype,"reference_name":reference_name,"recipients": eamaail_doc.recipient,"sender": frappe.session.user})
    doc.save(ignore_permissions=True)
    eamaail_doc.related_communication=doc.name
    eamaail_doc.save(ignore_permissions=True)


    # linked_comm= relink(doc.name, reference_doctype, reference_name)

 


def relink(name, reference_doctype=None, reference_name=None):
	frappe.db.sql(
		"""update
			`tabCommunication`
		set
			reference_doctype = %s,
			reference_name = %s,
			status = "Linked"
		where
			communication_type = "Communication" and
			name = %s""",
		(reference_doctype, reference_name, name),
	)


