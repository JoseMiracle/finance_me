from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from finance.accounts.tokens import account_activation_token


def account_activation_mail(user, current_site_domain, generated_otp, full_name):
     context = {
          'full_name': full_name,
          'otp': generated_otp,
          'current_site_domain': current_site_domain,
          'uid':urlsafe_base64_encode(force_bytes(user.pk)),
          'token':account_activation_token.make_token(user),
     }
     html_message = render_to_string('accounts/account_activation.html', context=context)
     plain_message = strip_tags(html_message)
     email = EmailMultiAlternatives(
        subject="Account Activation",
        to=[user.email],
        body=plain_message,
        from_email="admin@mail.com"
    )
     email.attach_alternative(html_message, "text/html")
     email.send()


def sign_in_with_otp_activation_mail(email,full_name, generated_otp):
     context = {
          'full_name': full_name,
          'otp': generated_otp,
     }
     html_message = render_to_string('accounts/sign_in_with_otp.html', context=context)
     plain_message = strip_tags(html_message)
     email = EmailMultiAlternatives(
        subject="OTP For Sign in",
        to=[email],
        body=plain_message,
        from_email="admin@mail.com"
    )
     email.attach_alternative(html_message, "text/html")
     email.send()


def otp_for_sign_in(email, username, generated_otp):
     send_mail(
        subject="Your Sign-in OTP for Finance Me",
        message= render_to_string('accounts/otp_for_sign_in.html', {'username': username, 'otp_code': generated_otp}),
        recipient_list=[email],
        from_email="admin@mail.com"
    )