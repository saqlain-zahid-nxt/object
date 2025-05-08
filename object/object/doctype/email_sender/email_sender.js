// Copyright (c) 2025, nextash and contributors
// For license information, please see license.txt

frappe.ui.form.on('Email Sender', {
	refresh: function (frm) {
		if (frm.doc.reference_doctype && frm.doc.reference_name) {
			frm.add_custom_button(__(frm.doc.reference_name), function () {
				frappe.set_route("Form", frm.doc.reference_doctype, frm.doc.reference_name);
			});
		}
		frm.add_custom_button(__("Relink"), function () {
			frm.trigger("show_relink_dialog");
		});

		frm.add_custom_button('Reply', () => {
			let d = new frappe.ui.Dialog({
				title: 'Reply to Email',
				fields: [
					{ label: 'Subject', fieldname: 'subject', fieldtype: 'Data', reqd: 1 },
					{ label: 'Message', fieldname: 'message', fieldtype: 'Text Editor', reqd: 1 }
				],
				primary_action_label: 'Send Reply',
				primary_action(values) {
					frappe.call({
						method: 'object.object.doctype.email_sender.email_sender.reply',
						args: {
							email_sender_name: frm.doc.name,
							subject: values.subject,
							message: values.message
						},
						callback: () => {
							frappe.msgprint('Reply sent');
							d.hide();
						}
					});
				}
			});
			d.show();
		});

	},
	show_relink_dialog: function (frm) {
		var d = new frappe.ui.Dialog({
			title: __("Relink Communication"),
			fields: [
				{
					fieldtype: "Link",
					options: "DocType",
					label: __("Reference Doctype"),
					fieldname: "reference_doctype",
					get_query: function () {
						return { query: "frappe.email.get_communication_doctype" };
					},
				},
				{
					fieldtype: "Dynamic Link",
					options: "reference_doctype",
					label: __("Reference Name"),
					fieldname: "reference_name",
				},
			],
		});
		d.set_value("reference_doctype", frm.doc.reference_doctype);
		d.set_value("reference_name", frm.doc.reference_name);
		d.set_primary_action(__("Relink"), function () {
			var values = d.get_values();
			if (values) {
				frappe.confirm(
					__("Are you sure you want to relink this communication to {0}?", [
						values["reference_name"],
					]),
					function () {
						d.hide();
						frappe.call({
							method: "object.object.doctype.email_sender.email_sender.relink_and_send_email",
							args: {
								docname: frm.doc.name,
								reference_doctype: values["reference_doctype"],
								reference_name: values["reference_name"],
							},
							callback: function () {
								frm.refresh();
							},
						});
					},
					function () {
						frappe.show_alert({
							message: __("Document not Relinked"),
							indicator: "info",
						});
					}
				);
			}
		});
		d.show();
	},
});
