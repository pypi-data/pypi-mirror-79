import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as bs


class Email:
    
    # Login details
    EMAIL = os.environ.get('EMAIL_USER')
    PASSWORD = os.environ.get('EMAIL_PASS')
    
    
    SMTP_SERVER = 'smtp.gmail.com' # Server info
    PORT = 465 # SSL port

    FROM = "noreply@demo.com"
    TO = EMAIL

   

    def __init__(self, product_name, price, url):
        self.product_name = product_name
        self.price = price
        self.url = url        
        self.subject = product_name
        # Plain text message
        self.msg = f"""
        {product_name} has reached {price}! Click here: {url}.
        """
        # Html message
        self.html = f"""
        <html>
            <head>
                <body>
                <p>{product_name} is now at {price}! Click <a href="{url}">here</a>.</p>                
                </body>
            </head> 
        </html>
        
        """

    # log in to server and send email
    def send_email(self):
        try:
            # Set up MIMEMultipart message object info
            msg = MIMEMultipart("alternative")
            msg["From"] = self.FROM
            msg["To"] = self.TO
            msg["Subject"] = self.product_name

            # Plain text info
            text_portion = MIMEText(self.msg, "plain")
            # HTML info
            html_portion = MIMEText(self.html, "html")

            # Attach text/html to message
            msg.attach(text_portion)
            msg.attach(html_portion)

            # Create a secure SSL context
            context = ssl.create_default_context()
            
            # Log in to server and send email
            with smtplib.SMTP_SSL(self.SMTP_SERVER, self.PORT, context=context) as server:
                server.login(self.EMAIL, self.PASSWORD)
                server.sendmail(self.FROM, self.TO, msg.as_string())
            # Notify user
            print('Email sent!')   
        
        except smtplib.SMTPException as e:
            print(e)
        