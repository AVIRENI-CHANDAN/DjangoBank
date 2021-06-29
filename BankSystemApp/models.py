from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import datetime
import re
from datetime import datetime

# Create your models here.
def getAccountNoNow():
    return "SB%sA"%("".join(re.split(r'-| |:|\.',datetime.now().__str__())))
class Account(models.Model):
    """
    The account for the users in this banking application.
    """
    ACCOUNT_TYPE_CHOICES = (
        (1,"Savings"),
        (2,"Current")
    )
    ACCOUNT_TYPE_DICT = dict(ACCOUNT_TYPE_CHOICES)
    id = models.AutoField(primary_key=True)
    # As on every save, saving the account_no from there is able to modify on every update
    # So it can be rectified using lambda function as default with a method redirection.
    # This enables us to use the account_no as per our wish but with only one
    # initiation of the account_no field.
    account_no = models.CharField(default = getAccountNoNow, editable=False,max_length=50,unique=True)
    account_type = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES,default=1)
    amount = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Account"
        ordering = ("timestamp",)
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    def __str__(self):
        return f"{self.account_no}({self.ACCOUNT_TYPE_DICT[self.account_type]})"
    def save(self,*args, **kwargs):
        super(Account, self).save(*args, **kwargs)

def getLoanAccountNoNow():
    return "SB%sL"%("".join(re.split(r'-| |:|\.',datetime.now().__str__())))
class LoanAccount(models.Model):
    """
    The loan account for the users in this banking application.
    """
    account_no = models.CharField(default= getLoanAccountNoNow, editable=False,max_length=50,unique=True)
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "LoanAccount"
        ordering = ['timestamp']
        verbose_name = 'LoanAccount'
        verbose_name_plural = 'LoanAccounts'
    def __str__(self):
        return self.account_no
    # def save(self,*args, **kwargs):
    #     self.bank_account = ClientUser.objects.get(loan_accounts=self.id).account
    #     super(LoanAccount, self).save(*args, **kwargs)


class CustomUser(AbstractUser):
    """
    This is a user base model for Staff and Clients in the application.
    """
    citizenship_card_number = models.CharField(max_length=50,unique=True,verbose_name="Identity proof id")
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10,unique=True)
    address = models.TextField(max_length=255)
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255,null=False,default="")
    email = models.EmailField(max_length=255,unique=True)
    email_valid = models.BooleanField(default=False,editable=False)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "Custom_user"
        ordering = ['full_name']
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
    def save(self,*args, **kwargs):
        if not "sha" in self.password:
            self.set_password(self.password)
        super(CustomUser,self).save(*args, **kwargs)

class ClientUser(CustomUser):
    """
    The client user is the consumer of the bank services of this application.
    """
    account = models.ForeignKey(Account,on_delete=models.CASCADE,unique=True)
    loan_accounts = models.ForeignKey(LoanAccount,on_delete=models.SET_NULL,blank=True,null=True)
    # loan_accounts = models.ManyToManyField(LoanAccount,blank=True,null=True)
    class Meta:
        db_table = "Clients"
        ordering = ['account__id']
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    def save(self,*args, **kwargs):
        # print("The account information received is:",self.account)
        # print("The loan accounts objects data received are:",self.loan_accounts)
        # print("The all loan accounts objects received are:",self.loan_accounts.all())
        # for i in self.loan_accounts.all():
            # print(i)
            # i.save()
        print("The loan accounts are:",self.loan_accounts)
        if self.loan_accounts is not None:
            self.loan_accounts.save()
        super(ClientUser, self).save(*args, **kwargs)
        # clientobj = ClientUser.objects.get(id=self.pk)
        # print(clientobj.loan_accounts)
        # print(clientobj.clientloans_set)

def getEmpIdNow():
    return "SBEMP%s"%("".join(re.split(r'-| |:|\.',datetime.now().__str__())))
class StaffUser(CustomUser):
    """
    The Staff user is the staff of the bank.
    """
    emp_id = models.CharField(default= getEmpIdNow,editable=False,unique=True,max_length=50)
    class Meta:
        db_table = "BankStaff"
        ordering = ['emp_id']
        verbose_name = "Employee"
        verbose_name_plural = "Staff"
    def save(self,*args, **kwargs):
        super(StaffUser, self).save(*args, **kwargs)

class TransactionRecord(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,default="")
    toacc = models.ForeignKey(Account,on_delete=models.DO_NOTHING,default="")
    description = models.CharField(max_length=1250)
    timestamp = models.TimeField(auto_now_add=True)
    class Meta:
        db_table = "Transactions"
        ordering = ['timestamp']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

class Record(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,default="")
    description = models.CharField(max_length=1250)
    timestamp = models.TimeField(auto_now_add=True)
    class Meta:
        db_table = "ApplicationRecords"
        ordering = ("timestamp",)
        verbose_name = "ApplicationRecord"
        verbose_name_plural = "ApplicationRecords"