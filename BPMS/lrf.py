from django.shortcuts import render
from .models import *
from datetime import datetime
from random import randint



def login(request):
    if request.session:
        request.session.flush()
    return render(request, 'BPMS/login.html')


def signup(request):
    return render(request, 'BPMS/register.html')


def forapproval(request):
    if request.method == 'POST':
        if request.POST['name'] and request.POST['address'] and request.POST['email'] and request.POST['telephone'] and request.POST['contact_person'] and request.POST['Designation'] and request.POST['con_person_telephone'] and request.POST['username'] and request.POST['pwd_original'] and request.POST['pwd_retype']:
            if not users.objects.filter(u_user_id = request.POST['username']):
                if request.POST['pwd_original'] == request.POST['pwd_retype']:
                    def mc_id_gen(line):
                        count = 0
                        line = request.POST['name']
                        words = line.split(" ")
                        no_space = list(filter(None, words))
                        nick = ""
                        for i in line:
                            if (i.isspace()):
                                count = count + 1

                        for word in no_space:
                            nick += word[0].upper()

                        while mc_details.objects.filter(mc_id=nick):
                            nick += str(randint(1, 9))

                        return nick

                    mc_register = mc_details()
                    mc_register.mc_id = mc_id_gen(request.POST['name'])
                    mc_register.mc_name = request.POST['name']
                    mc_register.mc_address = request.POST['address']
                    mc_register.mc_email = request.POST['email']
                    mc_register.mc_main_tele = request.POST['telephone']
                    mc_register.mc_contact_person = request.POST['contact_person']
                    mc_register.mc_designation = request.POST['Designation']
                    mc_register.mc_contact_person_mob = request.POST['con_person_telephone']
                    mc_register.mc_registered_date = datetime.now()
                    user_register = users()
                    user_register.u_user_id = request.POST['username']
                    user_register.u_mc_id = mc_register
                    user_register.u_pwd = request.POST['pwd_original']
                    user_register.u_level = "admin"
                    user_register.u_acc_status = "pending"
                    tax_reg = sub_tax()
                    tax_reg.sub_tax_id=mc_register.mc_id+"NOTAX"
                    tax_reg.sub_tax_amount=0
                    tax_reg.sub_tax_default=0
                    tax_reg.sub_mc_id=mc_register

                    mc_register.save()
                    tax_reg.save()
                    user_register.save()

                    return render(request, 'BPMS/login.html', {'message1': "Successfully Registered!", 'message2': "Waiting for the Approval."})

                else:
                    return render(request, 'BPMS/register.html', {'error_message': "Password doesn't match", 'f_data':request.POST})
            else:
                return render(request, 'BPMS/register.html', {'error_message': "Username already in use", 'f_data':request.POST})

        else:
            return render(request, 'BPMS/register.html', {'error_message': "Form incomplete"})
    else:
        return render(request, 'BPMS/register.html')


def login_verify(request):
    if request.POST['username'] and request.POST['pwd']:
        temp_pwd = ""
        try:
            temp_pwd = users.objects.get(u_user_id = request.POST['username']).u_pwd
        except:
            return render(request, 'BPMS/login.html', {'error_message': 'Username or Password incorrect!'})
        else:
            if request.POST['pwd'] == temp_pwd:
                if users.objects.get(u_user_id = request.POST['username']).u_acc_status == "pending":
                    return render(request, 'BPMS/login.html',{'message3': "Pending approval!", 'message4': "Please contact system administrator."})
                elif users.objects.get(u_user_id = request.POST['username']).u_acc_status == "approved":
                    #return render(request, 'BPMS/profile.html', {'user': users.objects.get(u_user_id = request.POST['username'])})
                    #https://docs.djangoproject.com/en/3.0/topics/security/#user-uploaded-content-security
                    #https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
                    #https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
                    request.session.set_expiry(28800)
                    request.session['u_name'] = request.POST['username']

                    return render(request, 'BPMS/dash.html', {'user_d':users.objects.get(u_user_id=request.session['u_name']),'page_title':'Dashboard'})

            else:
                return render(request, 'BPMS/login.html', {'error_message': 'Username or Password incorrect!'})
    else:
        return render(request, 'BPMS/login.html', {'error_message':'Login credentials incomplete!'})




