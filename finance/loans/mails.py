from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def request_for_guarantorship_mail(current_site_domain,user,loan_guarantor, loan_id, loan_amount):
    print(current_site_domain)
    context = { 
                'domain': current_site_domain,
                'user': user,
                'loan_amount': loan_amount,
                'loan_guarantor':loan_guarantor,
                'loan_id': loan_id
            }
    html_message = render_to_string('loans/request_for_guarantor_for_loan.html', context=context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=" Loan Guarantor Request",
        to=[loan_guarantor.email],
        body=plain_message,
        from_email="admin@mail.com"
    )

    
    email.attach_alternative(html_message, "text/html")
    email.send()



def guarantor_decision_for_loan_mail(requestor_full_name, loan_guarantor, loan_amount):
    context = {'requestor_full_name': requestor_full_name,
                'loan_amount': loan_amount,
                'guarantor':loan_guarantor 
            }
    html_message = render_to_string('loans/guarantor_decision_for_loan_request.html', context=context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject="Guarantor Decision",
        to=[loan_guarantor.email],
        body=plain_message,
        from_email="admin@mail.com"
    )

    email.attach_alternative(html_message, "text/html")
    email.send()


def loan_request_decision_mail(request_for_loan_obj):
    context = {
                'request_for_loan_obj': request_for_loan_obj,
            }
    html_message = render_to_string('loans/loan_request_decision.html', context=context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject="LOAN DECISION",
        to=[request_for_loan_obj.user.email],
        body=plain_message,
        from_email="admin@mail.com"
    )

    email.attach_alternative(html_message, "text/html")
    email.send()
