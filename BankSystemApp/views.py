from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import ClientUser,StaffUser,Account

# Create your views here.
def userlogin(req):
    if req.user.is_authenticated:
        try:
            if ClientUser.objects.get(customuser_ptr_id=req.user.id):
                # return HttpResponse(f"ClientUser ({req.user.full_name}) is authenticated already") 
                return redirect('clienthomePage')
        except:
            pass

        try:
            if StaffUser.objects.get(customuser_ptr_id=req.user.id):
                return HttpResponse("StaffUser ({req.user.full_name}) is authenticated already")
        except:
            pass

        # return HttpResponse(f"User{req.user.id} {req.user} is authenticated already")
        return redirect("/administrator")

    if req.method == 'GET' and not req.user.is_authenticated:
        return render(req,'staff/login.html')
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            try:
                if ClientUser.objects.get(customuser_ptr_id=req.user.id):
                    return redirect('clienthomePage')
            except:
                pass

            try:
                if StaffUser.objects.get(customuser_ptr_id=req.user.id):
                    return HttpResponse("StaffUser ({req.user.full_name}) is authenticated already")
            except:
                pass
        else:
            return HttpResponse("User not logged in")
        return HttpResponse(f"The user name and password are {username} <br> {password}")

@login_required(login_url="/")
def userlogout(req):
    if req.user is not None:
        # message = f"The user {req.user} logged out!"
        logout(req)
        # return HttpResponse(message)
        return redirect("/")

@login_required(login_url='/')
def clientHome(req,*args, **kwargs):
    if req.method == "GET":
        context = {
            "account":ClientUser.objects.get(customuser_ptr_id = req.user.id).account,
            # "loan_accounts":ClientUser.objects.get(customuser_ptr_id = req.user.id).loan_accounts.all()
            "loan_accounts":ClientUser.objects.get(customuser_ptr_id = req.user.id).loan_accounts,
        }
        # messages.info(req,"text message")
        return render(req,"staff/home.html",context=context)
    if req.method == "POST":
        target_acc = req.POST.get('accountno')
        try:
            amount = int(req.POST.get('amount'))
        except:
            amount = 0
        csrf_token = req.POST.get('csrf_token')
        print(csrf_token)
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        # print(user.get_username)
        # print(user.password)
        if user is not None:
            client = ClientUser.objects.get(customuser_ptr_id = req.user.id)
            # print("The user details are:",client)
            # print("The target account number is:",target_acc)
            selfacc = client.account
            targetacc = Account.objects.get(account_no=target_acc)
            # print("The target account is:",targetacc)
            if selfacc.amount >= amount:
                targetacc.amount = targetacc.amount + amount
                selfacc.amount = selfacc.amount - amount
                targetacc.save()
                selfacc.save()
                messages.success(req,"Transaction done!")
            else:
                messages.warning(req,"Insuffiecient funds")
            # print(client.account.account_no)
        else:
            messages.error(req,"Wrong credentials")

        return redirect("clienthomePage")