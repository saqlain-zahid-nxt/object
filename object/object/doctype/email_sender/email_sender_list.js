frappe.listview_settings['Email Sender'] = {
    onload: function(listview) {
        listview.page.add_inner_button('New Email', () => {
            const d = new frappe.ui.Dialog({
                title: 'Send Email',
                fields: [
                    {
                        label: 'To',
                        fieldname: 'recipient',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'Subject',
                        fieldname: 'subject',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'Message',
                        fieldname: 'message',
                        fieldtype: 'Text Editor',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Send',
                primary_action(values) {
                    frappe.call({
                        method: 'object.object.doctype.email_sender.email_sender.send_email_and_save',
                        args: {
                            data: values
                        },
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.msgprint('Email Sent and Record Saved');
                                d.hide();
                                listview.refresh();
                            }
                        }
                    });
                }
            });
            d.show();
        });
    }
};