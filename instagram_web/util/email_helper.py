import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def donation_email(receiver, amount):
    print(receiver.email)
    message = Mail(
        from_email = 'wingtat.calix@gmail.com',
        to_emails = 'wingtat.calix@gmail.com',
        subject = 'Thanks for your donation!',
        html_content = f'<h1> Dear {receiver.username}, </h1><br/>Thank you for your recent donation of {amount} USD! <br/><br/><h1>NEXTAGRAM</h1>'
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))