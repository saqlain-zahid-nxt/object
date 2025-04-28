// frappe.ui.form.on("Making User", {
//     refresh: function (frm) {
//         // Button to create user
//         frm.add_custom_button('Create User', () => {
//             if (!frm.doc.email || !frm.doc.name1) {
//                 frappe.msgprint(__('Please enter both Email and Name'));
//                 return;
//             }

//             frappe.call({
//                 method: 'object.object.doctype.making_user.making_user.create_user_from_request',
//                 args: {
//                     email: frm.doc.email,
//                     name1: frm.doc.name1
//                 },
//                 callback: function (r) {
//                     if (!r.exc) {
//                         frappe.msgprint(__('User created successfully'));
//                     }
//                 }
//             });
//         });

//         // Button to verify OTP
//         frm.add_custom_button('Verify OTP', () => {
//             frappe.prompt([
//                 {
//                     label: 'Email',
//                     fieldname: 'email',
//                     fieldtype: 'Data',
//                     reqd: 1
//                 },
//                 {
//                     label: 'OTP',
//                     fieldname: 'otp',
//                     fieldtype: 'Data',
//                     reqd: 1
//                 }
//             ], (values) => {
//                 frappe.call({
//                     method: 'object.object.doctype.making_user.making_user.verify_otp',  // replace with your actual path
//                     args: {
//                         email: values.email,
//                         otp_to_verify: values.otp
//                     },
//                     callback: function (r) {
//                         if (r.message && r.message.success) {
//                             frappe.msgprint(__('OTP verified successfully.'));
//                         } else {
//                             frappe.msgprint(__('Invalid OTP.'));
//                         }
//                     },
//                     error: function (err) {
//                         frappe.msgprint(__('OTP verification failed.'));
//                     }
//                 });
//             }, 'Verify OTP', 'Submit');
//         });

//     }
// });
