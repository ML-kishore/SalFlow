from django.db import models

# Create your models here.
class Employee(models.Model):
    emp_id = models.CharField(max_length=10,unique=True),
    dept = models.CharField(max_length=150,null=False),
    designation = models.CharField(max_length=150,null=False),
    shift = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.emp_id} - {self.dept}"
    

class PayrollBatch(models.Model):
    month=models.CharField(max_length=50)
    year = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=50,default='UPLOADED')

    def __str__(self):
        return f"{self.month} - {self.year}"


class PayrollRecord(models.Model):
    emp_name = models.ForeignKey(Employee,on_delete=models.PROTECT)
    batch = models.ForeignKey(PayrollBatch,on_delete=models.PROTECT)
    basic = models.DecimalField(max_digits=10,decimal_places=2)
    da = models.DecimalField(max_digits=10,decimal_places=2)
    hra = models.DecimalField(max_digits=10,decimal_places=2)
    att_allowance = models.DecimalField(max_digits=10,decimal_places=2)
    wa = models.DecimalField(max_digits=10,decimal_places=2)
    conveyance = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    pf = models.DecimalField(max_digits=10,decimal_places=2)
    esi= models.DecimalField(max_digits=10,decimal_places=2)
    canteen = models.DecimalField(max_digits=10,decimal_places=2)
    deductions = models.DecimalField(max_digits=10,decimal_places=2)
    net_salary = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.emp_name} -- {self.batch.month}-{self.batch.year}"

