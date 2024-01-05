from django.core.mail import send_mail
from django.template.loader import render_to_string

def otp_for_account_activation(email, generated_otp):
    send_mail(
        subject="Activation of account",
        message=f"Thanks for signing up, here is your otp: {generated_otp}",
        recipient_list=[email],
        from_email="admin@mail.com"
    )

def otp_for_sign_in(email, username, generated_otp):
     send_mail(
        subject="Your Sign-in OTP for Finance Me",
        message= render_to_string('accounts/otp_for_sign_in.html', {'username': username, 'otp_code': generated_otp}),
        recipient_list=[email],
        from_email="admin@mail.com"
    )