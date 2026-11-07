import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "SalFlow.settings"
)

django.setup()

from django.core.mail import EmailMessage
from app.models import PayrollRecord

records = PayrollRecord.objects.filter(month=10,year=2026).exclude(mail_id__isnull=True).exclude(mail_id="").exclude(payslip_pdf="")

sent = 0
skipped = 0

for record in records:

    if not record.payslip_pdf:
        skipped += 1
        continue

    try:
        # Read existing PDF
        record.payslip_pdf.open("rb")
        try:
            pdf_data = record.payslip_pdf.read()
        finally:
            record.payslip_pdf.close()

        # Create individual email
        email = EmailMessage(
            subject=f"Salary Slip - {record.month}/{record.year}",
            body=f"""Dear {record.name},Please find your salary slip attached.Regards,EMCTECH PRIVATE LIMITED """,
            from_email=None,
            to=[record.mail_id]
        )

        # Attach employee's PDF
        email.attach(f"salary_slip_{record.emp_id}.pdf",pdf_data,"application/pdf")

        email.send(fail_silently=False)
        sent += 1

    except Exception as e:
        print(f"Failed for {record.emp_id}: {e}")

print("Emails sent:", sent)
print("Skipped:", skipped)