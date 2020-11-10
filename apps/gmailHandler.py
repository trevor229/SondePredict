import smtplib

# Import the email modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define email addresses to use
addr_to   = 'your.email@gmail.com'
addr_from = "your.send.email@gmail.com"

def mail(SUBJ,HTML):
    # Define SMTP email server details
    smtp_server = 'smtp.gmail.com'
    smtp_user   = 'your.send.email@gmail.com'
    smtp_pass   = 'PASSWORD'

    # Construct email
    msg = MIMEMultipart('alternative')
    msg['To'] = addr_to
    msg['From'] = addr_from
    msg['Subject'] = SUBJ

    # Create the body of the message (a plain-text and an HTML version).
    text = "This is the fallback text, if this shows up then fix whatever went wrong."

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via an SMTP server
    s = smtplib.SMTP(smtp_server,587)
    s.ehlo()
    s.starttls()
    s.login(smtp_user,smtp_pass)

    try:
        s.sendmail(addr_from, addr_to, msg.as_string())
        print ('Email Sent!')
    except:
        print ('Error Sending Mail')

    s.quit()

