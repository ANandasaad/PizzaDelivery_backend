from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType
import logging

from config.envFile import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_PORT, MAIL_SERVER


async def send_notification_otp(email, otp):
    try:
        conf = ConnectionConfig(
            MAIL_USERNAME=MAIL_USERNAME,
            MAIL_PASSWORD=MAIL_PASSWORD,
            MAIL_FROM=MAIL_FROM,
            MAIL_PORT=MAIL_PORT,
            MAIL_SERVER=MAIL_SERVER,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        message = MessageSchema(
            subject="OTP",
            recipients=[email],
            body=f"Your OTP is {otp}",
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return {"message": "Failed to send email", "error": str(e)}