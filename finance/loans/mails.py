from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def request_for_guarantorship_mail(user,loan_guarantor, loan_id, loan_amount):
    context = {'user': user,
                'loan_amount': loan_amount,
                'loan_guarantor':loan_guarantor,
                'loan_id': loan_id
            }
    html_message = render_to_string('loans/request_for_loan.html', context=context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=" Loan Guarantor Request",
        to=[loan_guarantor.email],
        body=plain_message,
        from_email="admin@mail.com"
    )

    
    email.attach_alternative(html_message, "text/html")
    email.send()