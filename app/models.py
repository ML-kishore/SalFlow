from django.db import models

class PayrollRecord(models.Model):
    emp_id = models.CharField(unique=True,max_length=6)
    name=models.CharField(null=False,max_length=150)
    dept = models.CharField(null=False,max_length=100)
    desg = models.CharField(null=False,max_length=100)
    gross = models.DecimalField(decimal_places=2,max_digits=10)
    basic = models.DecimalField(decimal_places=2,max_digits=10)
    hra = models.DecimalField(decimal_places=2,max_digits=10)
    da = models.DecimalField(decimal_places=2,max_digits=10)
    att_allowance = models.DecimalField(decimal_places=2,max_digits=10)
    wa = models.DecimalField(decimal_places=2,max_digits=10)
    pf = models.DecimalField(decimal_places=2,max_digits=10)
    esi = models.DecimalField(decimal_places=2,max_digits=10)
    tax = models.DecimalField(decimal_places=2,max_digits=10)
    deductions = models.DecimalField(decimal_places=2,max_digits=10)
    incentives = models.DecimalField(decimal_places=2,max_digits=10)
    net_salary = models.DecimalField(decimal_places=2,max_digits=10)
    month = models.IntegerField()
    year = models.IntegerField()
    payslip_pdf = models.FileField(upload_to='salary_slips/',null=True,blank=True)
    mail_id = models.EmailField(null=True)

    def __str__(self):
        return f"{self.emp_id} - {self.month}{self.year}"
    