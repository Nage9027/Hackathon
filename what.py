import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail SMTP server and port
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Sender's and receiver's email addresses
sender_email = "your_email@gmail.com"  # Replace with your email address
receiver_email = "receiver_email@example.com"  # Replace with the recipient's email address

# Email subject and body
subject = "Test Email from Python"
body = "Hello, this is a test email sent using Python!"

# Email login credentials (use app-specific password if 2FA enabled)
password = "your_password"  # Replace with your email password or app password

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the body of the email to the message
message.attach(MIMEText(body, "plain"))

# Connect to the Gmail SMTP server
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start TLS encryption
        server.login(sender_email, password)  # Log in to the server
        text = message.as_string()  # Convert the message to string
        server.sendmail(sender_email, receiver_email, text)  # Send the email

    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {str(e)}")
