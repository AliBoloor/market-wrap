from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_report_email(report_path: Path, report_url: str) -> None:
    """Send a lightweight delivery email using credentials supplied at runtime."""
    username = os.environ["SMTP_USERNAME"]
    password = os.environ["SMTP_PASSWORD"]
    recipient = os.environ["REPORT_EMAIL_TO"]
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "465"))

    message = EmailMessage()
    message["Subject"] = f"Pre-Market Wrap — {report_path.parent.name}"
    message["From"] = username
    message["To"] = recipient
    message.set_content(
        "Your pre-market report is ready.\n\n"
        f"Open the latest report: {report_url}\n\n"
        "This automated report is informational and is not investment advice."
    )
    message.add_alternative(
        f"""<!doctype html><html><body style="font-family:system-ui,sans-serif;color:#152033">
        <h2>Your pre-market report is ready</h2>
        <p><a style="background:#1d4ed8;color:white;padding:10px 16px;text-decoration:none;border-radius:6px" href="{report_url}">Open Market Wrap</a></p>
        <p style="color:#64748b;font-size:12px">This automated report is informational and is not investment advice.</p>
        </body></html>""",
        subtype="html",
    )
    with smtplib.SMTP_SSL(host, port, timeout=30) as smtp:
        smtp.login(username, password)
        smtp.send_message(message)
