from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from collections import OrderedDict
from django.db.models import Q



def settings_pf(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    tax_details = sub_tax.objects.get(sub_mc_id=user_d.u_mc_id)
    mc_id_len = len(user_d.u_mc_id.mc_id)
    str_slice = str(mc_id_len) + ":"
    if (request.method == "POST"):
        mc_register = mc_details.objects.get(mc_id = user_d.u_mc_id.mc_id)
        mc_register.mc_name = request.POST['name']
        mc_register.mc_address = request.POST['address']
        mc_register.mc_email = request.POST['email']
        mc_register.mc_main_tele = request.POST['telephone']
        mc_register.mc_contact_person = request.POST['contact_person']
        mc_register.mc_designation = request.POST['Designation']
        mc_register.mc_contact_person_mob = request.POST['con_person_telephone']
        mc_register.mc_currency = request.POST['currency']
        tax_reg = sub_tax()
        if request.POST['tax_id'] == '':
            tax_reg.sub_tax_id = user_d.u_mc_id.mc_id + "NOTAX"
            tax_reg.sub_tax_amount = 0
        else:
            tax_reg.sub_tax_id = user_d.u_mc_id.mc_id + str(request.POST['tax_id'])
            tax_reg.sub_tax_amount = float(request.POST['tax_amount'])
        tax_reg.sub_tax_default = int(request.POST.get('tax_default', tax_details.sub_tax_default))
        tax_reg.sub_mc_id = user_d.u_mc_id
        mc_register.save()
        tax_details.delete()
        tax_reg.save()

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    tax_details = sub_tax.objects.get(sub_mc_id=user_d.u_mc_id)
    return render(request, 'BPMS/settings_prof.html', {'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'str_slice':str_slice,'tax_details':tax_details, 'page_title':'Settings'})


