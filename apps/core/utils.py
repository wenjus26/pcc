from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_pcc_email(subject, template_name, context, recipient_list):
    """
    Helper function to send branded HTML emails for PCC Platform.
    """
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
