from django.contrib import admin
from .models import Account, ClientUser, StaffUser, TransactionRecord, LoanAccount, CustomUser
from django.utils.translation import gettext_lazy
from django.db.models import QuerySet
from django import forms

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    fields = [("account_type", "amount")]
    list_display = ["account_no", "account_type","timestamp"]
    class Media:
        css = {}
        js = []
        

class LoanAccountAdmin(admin.ModelAdmin):
    fields = ["amount"]
    list_display = ["account_no","amount","timestamp","client_name"]
    class Media:
        css = {}
        js = []
    def client_name(self,obj):
        return ClientUser.objects.get(loan_accounts = obj.id).full_name
    


class ClientUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Client User", {
            "fields": (("first_name","last_name",'full_name'),('citizenship_card_number','phone_number'),('account','username','password'),'address',('email',"email_valid")),
        }),
        ('Advanced options', {
            'classes': ('show',),
            'fields': ('loan_accounts',),
        }),
    )
    list_display = ["citizenship_card_number", "full_name",'email',"account","loans"]
    readonly_fields = ('email_valid',)
    class Media:
        css = {}
        js = []
    def loans(self,obj):
        # Can be used for only ManyToManyField
        # string = ""
        # print("The loans are:",obj.loan_accounts.all())
        # for i in obj.loan_accounts.all():
        #     string+=i.account_no+"-->"+str(i.amount)+"; "
        # return string
        # 
        if obj.loan_accounts is None:
            return ""
        return obj.loan_accounts.__str__()
    def get_form(self, request, obj=None, **kwargs):
        form = super(ClientUserAdmin, self).get_form(request, obj, **kwargs)
        print("The client user form object from Admins.py ClientUserAdmin",form)
        print(form.base_fields['loan_accounts'])
        for i in form.base_fields['loan_accounts'].choices:
            print("Choice:",i)
        try:
            # form.base_fields['loan_accounts'].choices = obj.loan_accounts.all()
            # form.base_fields['loan_accounts'].choices = ""
            print("line 62",form.base_fields['loan_accounts'].choices)
            # form.base_fields['loan_accounts'].choices = obj.loan_accounts
            print("line 64",form.base_fields['loan_accounts'].choices)
            # form.base_fields['loan_accounts'] = obj.loan_accounts
            # form.base_fields['loan_accounts'].disabled = True
            form.base_fields['loan_accounts'].value = obj.loan_accounts
            print("line 68")
            print("The loan acccounts are:",obj.loan_accounts)
        except:
            form.base_fields['loan_accounts'].value = ""
            # pass
        return form

class StaffUserAdmin(admin.ModelAdmin):
    fields = (('first_name','last_name','full_name'),('citizenship_card_number','phone_number'),'address',('username','password','email'))
    readonly_fields = ("emp_id",)
    list_display = ("citizenship_card_number","full_name",'phone_number','username','email')
    class Media:
        css = {}
        js = []

class TransactionRecordAdmin(admin.ModelAdmin):
    fields = ('user','description')
    readonly_fields = ("timestamp",)
    list_display = ('user','timestamp')
    class Media:
        css = {}
        js = []

class MyAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('Stark Banks application administration')
    # Text to put in each page's <h1>.
    site_header = gettext_lazy('Stark Banks Data Center')
    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Data Segments')
    # URL for the "View site" link at the top of each admin page. Generally the site of application.
    site_url = '/'

admin_site = MyAdminSite(name='myadmin')

# admin.site.register(Account,AccountAdmin)
# admin.site.register(ClientUser,ClientUserAdmin)
# admin.site.register(StaffUser,StaffUserAdmin)
# admin.site.register(TransactionRecord,TransactionRecordAdmin)
admin.site.register(CustomUser)

admin_site.register(Account,AccountAdmin)
admin_site.register(ClientUser,ClientUserAdmin)
admin_site.register(StaffUser,StaffUserAdmin)
admin_site.register(TransactionRecord,TransactionRecordAdmin)
admin_site.register(LoanAccount,LoanAccountAdmin)