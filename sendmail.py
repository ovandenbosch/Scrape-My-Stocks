import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date


def send_email(filename):
    from_add = "ovdbdeveloper@gmail.com"
    to_adds = ["fvandenbosch@sky.com",
              "kvandenbosch@sky.com",
              "beavdb@icloud.com",
              "boschy08@icloud.com"]
    me = "vanders06@icloud.com"
    for to_add in me:
        subject = "Financial Stock Report from " + str(date.today())

        msg = MIMEMultipart()
        msg["From"] = from_add
        msg["To"] = to_add
        msg["Subject"] = subject

        body = "<h4>FINANCIAL STOCK REPORT</h4><p>I hope that this stock report contains all the necessary information.</p>"
        msg.attach(MIMEText(body, "html"))

        my_file = open(filename, "rb")

        part = MIMEBase("application", "octet-stream")
        part.set_payload((my_file.read()))
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= " + filename)
        msg.attach(part)

        message = msg.as_string()

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("ovdbdeveloper@gmail.com", "jyvkwaoisuyncnsv")

        server.sendmail(from_add, to_add, message)

        server.quit()
