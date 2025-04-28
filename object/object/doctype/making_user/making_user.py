import frappe
# import random
# import json
# import time

@frappe.whitelist()
def create_user_from_request(email, name1):
    # Check if the user already exists
    if frappe.db.exists("User", email):
        frappe.throw("User with this email already exists.")

    # Create new User
    user = frappe.new_doc("User")
    user.email = email
    user.first_name = name1
    user.send_welcome_email = 0
    user.insert(ignore_permissions=True)

    return {"user": user.name, "created": True}


# def generate_otp():
#     return str(random.randint(100000, 999999))

# @frappe.whitelist()
# def create_user_from_request(email, name1):
#     if frappe.db.exists("User", email):
#         frappe.throw("User with this email already exists.")

#     user = frappe.new_doc("User")
#     user.email = email
#     user.first_name = name1
#     user.send_welcome_email = 0
#     user.insert(ignore_permissions=True)

#     otp = generate_otp()
#     otp_data = {
#         "otp": otp,
#         "expires_at": time.time() + 300  # 5 minutes expiry
#     }

#     # ✅ Store as JSON string
#     frappe.cache().set(f"otp:{email}", json.dumps(otp_data))

#     frappe.sendmail(
#         recipients=email,
#         subject="Your OTP Code",
#         message=f"Hi {name1},<br><br>Your OTP is: <b>{otp}</b>. It is valid for 5 minutes."
#     )

#     return {"user": user.name, "otp_sent": True}


# @frappe.whitelist()
# def verify_otp(email, otp_to_verify):
#     cached_data = frappe.cache().get(f"otp:{email}")
#     if cached_data:
#         cached_data = json.loads(cached_data)

#         current_time = time.time()
#         if current_time > cached_data["expires_at"]:
#             frappe.cache().delete(f"otp:{email}")  # ❌ Delete expired OTP
#             frappe.throw("OTP has expired.")

#         elif cached_data["otp"] == otp_to_verify:
#             frappe.cache().delete(f"otp:{email}")  # ✅ Delete used OTP
#             return {"success": True, "message": "OTP verified successfully."}

#         else:
#             frappe.throw("Invalid OTP.")
#     else:
#         frappe.throw("OTP not found or expired.")
