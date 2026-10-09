import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.celery_app import celery_app

@celery_app.task(bind=True, max_retries=3)
def generate_pdf_invoice(self, order_id: int) -> str:
    """Generates a PDF invoice file on disk."""
    try:
        os.makedirs("/tmp/invoices", exist_ok=True)
        file_path = f"/tmp/invoices/invoice_{order_id}.pdf"
        
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 750, f"ORDER INVOICE #{order_id}")
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, "Status: PAID")
        c.drawString(100, 700, "Thank you for your business!")
        c.save()
        
        return file_path
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)

@celery_app.task(bind=True, max_retries=3)
def send_transactional_email(self, pdf_path: str, recipient_email: str, order_id: int):
    """Sends order confirmation email with the generated PDF attached."""
    try:
        msg = MIMEMultipart()
        msg["From"] = os.getenv("SMTP_USER", "no-reply@store.com")
        msg["To"] = recipient_email
        msg["Subject"] = f"Your Invoice for Order #{order_id}"

        body = f"Hello,\n\nYour order #{order_id} has been processed successfully! See the attached receipt."
        msg.attach(MIMEText(body, "plain"))

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="invoice_{order_id}.pdf"')
                msg.attach(part)

        smtp_host = os.getenv("SMTP_HOST", "localhost")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER", ""), os.getenv("SMTP_PASSWORD", ""))
            server.send_message(msg)

        return f"Email delivered to {recipient_email}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)