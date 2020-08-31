frappe.ui.form.on("Purchase Order", "refresh", function(frm, cdt, cdn) {
    if (cur_frm.doc.docstatus == 1) {

        cur_frm.add_custom_button(__('Send Mail'), function() {
            if (cur_frm.doc.items[0].sales_order) {
                var titles = "Purchase Order :" + cur_frm.doc.name
                var email_list = get_email_list()
                var print_list = get_print_format(cur_frm.doc.doctype)
                var doctype = "Sales Order";
                var print_lists = get_print_format(doctype)
                var d = new frappe.ui.Dialog({
                    title: titles,

                    fields: [{
                            label: 'TO',
                            fieldname: 'recipients',
                            fieldtype: 'MultiSelect',
                            options: email_list
                        },
                        {
                            label: 'CC, BCC & EMAIL TEMPLATE',
                            fieldname: 'sec_1',
                            fieldtype: 'Section Break',
                            collapsible: 1
                        },
                        {
                            label: 'CC',
                            fieldname: 'cc',
                            fieldtype: 'MultiSelect',
                            options: email_list
                        },
                        {
                            label: 'BCC',
                            fieldname: 'bcc',
                            fieldtype: 'MultiSelect',
                            options: email_list
                        },
                        {
                            label: 'Email Templat',
                            fieldname: 'email_template',
                            fieldtype: 'Link',
                            options: "Email Template"
                        },
                        {
                            label: '',
                            fieldname: 'sec_2',
                            fieldtype: 'Section Break',

                        },
                        {
                            label: 'Subject',
                            fieldname: 'subject',
                            fieldtype: 'Data',
                            default: titles
                        }, {
                            label: '',
                            fieldname: 'sec_3',
                            fieldtype: 'Section Break',

                        },
                        {
                            label: 'Message',
                            fieldname: 'content',
                            fieldtype: 'Text Editor',

                        },
                        {
                            label: '',
                            fieldname: 'sec_3',
                            fieldtype: 'Section Break',

                        },
                        {
                            label: "Send me a copy",
                            fieldname: 'send_me_a_copy',
                            fieldtype: 'Check',
                        },
                        {
                            label: "Send Read Receipt",
                            fieldname: 'send_read_receipt',
                            fieldtype: 'Check',
                        },
                        {
                            label: "Attach Document Print",
                            fieldname: 'attach_document_print',
                            fieldtype: 'Check',
                        },
                        {
                            label: "Select Print Format",
                            fieldname: 'select_print_format',
                            fieldtype: 'Select',
                            options: print_list
                        },
                        {
                            label: "Select Languages",
                            fieldname: 'select_language',
                            fieldtype: 'Link',
                            options: "Language",
                            default: "English"
                        },
                        {
                            label: '',
                            fieldname: 'col_break',
                            fieldtype: 'Column Break',

                        },
                        {
                            label: "Select Attachments",
                            fieldname: "select_attachments",
                            fieldtype: "Attach"
                        },
                        {
                            label: "Sales Order",
                            fieldname: "sales_order",
                            fieldtype: "Link",
                            options: "Sales Order",
                            default: cur_frm.doc.items[0].sales_order,
                            read_only: 1

                        },
                        {
                            label: "Select Print Format",
                            fieldname: 'select_print_formats',
                            fieldtype: 'Select',
                            options: print_lists
                        },
                        {
                            label: "Select Languages",
                            fieldname: 'select_languages',
                            fieldtype: 'Link',
                            options: "Language",
                            default: "English"
                        },
                    ],
                    primary_action_label: 'Send',
                    primary_action(values) {
                        d.hide();
                        frappe.call({
                            method: 'plastex.api.send_mail',
                            args: {
                                "values": d.get_values(),
                                "docname": cur_frm.doc.name
                            },
                            async: false,
                            callback: function(r) {
                                email_list = r.message;

                            }
                        });
                    }

                })
                d.show();
            }else{
			frappe.throw("This "+cur_frm.doc.name+" Purchase Order is not linked with Sales Order ")
		}
        })
    }
})

function get_email_list() {
    var email_list = "";
    frappe.call({
        method: 'plastex.api.get_email_list',
        args: {

        },
        async: false,
        callback: function(r) {
            email_list = r.message;

        }
    });
    return email_list;
}

function get_print_format(doctype) {
    var print_list = "";
    frappe.call({
        method: 'plastex.api.get_print_format',
        args: {
            "doctype": doctype
        },
        async: false,
        callback: function(r) {
            print_list = r.message;

        }
    });
    return print_list
}
