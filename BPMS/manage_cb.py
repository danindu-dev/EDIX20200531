from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from collections import OrderedDict
from django.db.models import Q

def client_view(request):
    user_d = users.objects.get(u_user_id=request.session['u_name'])
    mc_id_len = len(user_d.u_mc_id.mc_id)
    item_data = sub_clients.objects.filter(Q(sub_mc_id=user_d.u_mc_id.mc_id) , Q(status=1))
    item_for_view = []
    for item in item_data:
        item_for_view.append({'id':item.sub_client_id,'name':item.sub_client_name, 'address':item.sub_address, 'tele':item.sub_tele, 'other':item.sub_contact_person})
    str_slice = str(mc_id_len) + ":"
    return render(request, 'BPMS/manage_view.html',
                  {'user_d': users.objects.get(u_user_id=request.session['u_name']), 'page_title': 'View Clients',
                   'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice, 'th_id':'Client ID',
                   'th_name':'Client Name', 'th_address':'Client Address', 'th_tel' : 'Contact Number',
                   'th_other':'Contact Person', 'e':'1'})


def bank_view(request):
    user_d = users.objects.get(u_user_id=request.session['u_name'])
    mc_id_len = len(user_d.u_mc_id.mc_id)
    item_data = sub_bank.objects.filter(Q(sub_mc_id=user_d.u_mc_id.mc_id) , Q(status=1))
    item_for_view = []
    for item in item_data:
        item_for_view.append({'id':item.sub_bank_id,'name':item.sub_bank_name, 'address':item.sub_bank_address, 'tele':item.sub_bank_tel, 'other':item.sub_bank_acc})
    str_slice = str(mc_id_len) + ":"
    return render(request, 'BPMS/manage_view.html',
                  {'user_d': users.objects.get(u_user_id=request.session['u_name']), 'page_title': 'View Banks',
                   'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice, 'th_id':'Bank ID',
                   'th_name':'Bank Name', 'th_address':'Bank Address', 'th_tel' : 'Contact Number',
                   'th_other':'Acc Number', 'e':'2'})

def d_save(request):
    user_d = users.objects.get(u_user_id=request.session['u_name'])
    mc_id_len = len(user_d.u_mc_id.mc_id)
    item_for_view = []
    str_slice=":"
    if (request.method == "POST"):

        if request.POST.get('e', '0') == '1':
            item = sub_clients.objects.get(sub_client_id=user_d.u_mc_id.mc_id + request.POST['item_id'])
            item_for_view.append({'id': item.sub_client_id, 'name': item.sub_client_name, 'address': item.sub_address,
                                  'tele': item.sub_tele, 'other': item.sub_contact_person})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_item.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                           'page_title': 'Client Details',
                           'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                           'th_id': 'Client ID',
                           'th_name': 'Client Name', 'th_address': 'Client Address', 'th_tel': 'Contact Number',
                           'th_other': 'Contact Person', 'frm_header': 'Client Details'})

        elif request.POST.get('e', '0') == '2':
            item = sub_bank.objects.get(sub_bank_id= user_d.u_mc_id.mc_id + request.POST['item_id'])
            item_for_view.append({'id':item.sub_bank_id,'name':item.sub_bank_name, 'address':item.sub_bank_address, 'tele':item.sub_bank_tel, 'other':item.sub_bank_acc})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_item.html',
                      {'user_d': users.objects.get(u_user_id=request.session['u_name']), 'page_title': 'Bank Details',
                       'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice, 'th_id':'Bank ID',
                   'th_name':'Bank Name', 'th_address':'Bank Address', 'th_tel' : 'Contact Number',
                   'th_other':'Acc Number', 'frm_header':'Bank Details'})

        elif request.POST.get('todo', '0') == 'update' and request.POST.get('item_type', '0') == 'client':
            item = sub_clients.objects.get(sub_client_id=user_d.u_mc_id.mc_id + request.POST['item_id'])
            item.sub_client_name = request.POST['item_name']
            item.sub_address = request.POST['item_address']
            item.sub_tele = request.POST['item_tel']
            item.sub_contact_person = request.POST['item_other']
            item.save()
            item = sub_clients.objects.get(sub_client_id=user_d.u_mc_id.mc_id + request.POST['item_id'])
            item_for_view.append({'id': item.sub_client_id, 'name': item.sub_client_name, 'address': item.sub_address,
                                  'tele': item.sub_tele, 'other': item.sub_contact_person})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_item.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                           'page_title': 'Client Details',
                           'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                           'th_id': 'Client ID',
                           'th_name': 'Client Name', 'th_address': 'Client Address', 'th_tel': 'Contact Number',
                           'th_other': 'Contact Person', 'frm_header': 'Client Details'})

        elif request.POST.get('todo', '0') == 'update' and request.POST.get('item_type', '0') == 'bank':
            item = sub_bank.objects.get(sub_bank_id=user_d.u_mc_id.mc_id + request.POST['item_id'])
            item.sub_bank_name = request.POST['item_name']
            item.sub_bank_address = request.POST['item_address']
            item.sub_bank_tel = request.POST['item_tel']
            item.sub_bank_acc = request.POST['item_other']
            item.save()
            item = sub_bank.objects.get(sub_bank_id=user_d.u_mc_id.mc_id + request.POST['item_id'])
            item_for_view.append({'id':item.sub_bank_id,'name':item.sub_bank_name, 'address':item.sub_bank_address, 'tele':item.sub_bank_tel, 'other':item.sub_bank_acc})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_item.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                           'page_title': 'Bank Details',
                       'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice, 'th_id':'Bank ID',
                   'th_name':'Bank Name', 'th_address':'Bank Address', 'th_tel' : 'Contact Number',
                   'th_other':'Acc Number', 'frm_header':'Bank Details'})

        elif request.POST.get('e', '0') == 'add2':
            item_for_view.append({'id':'','name':'', 'address':'', 'tele':'', 'other':''})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_item.html',
                      {'user_d': users.objects.get(u_user_id=request.session['u_name']),'page_title':'Add New Bank Acc',
                       'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice, 'th_id':'Bank ID',
                   'th_name':'Bank Name', 'th_address':'Bank Address', 'th_tel' : 'Contact Number',
                   'th_other':'Acc Number', 'frm_header':'Bank Details'})

        elif request.POST.get('e', '0') == 'add1':
            item_for_view.append({'id': '', 'name': '', 'address': '', 'tele': '', 'other': ''})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_item.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                           'page_title': 'Add New Client',
                           'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                           'th_id': 'Client ID',
                           'th_name': 'Client Name', 'th_address': 'Client Address', 'th_tel': 'Contact Number',
                           'th_other': 'Contact Person', 'frm_header': 'Client Details'})

        elif request.POST.get('todo', '0') == 'add' and request.POST.get('item_type', '0') == 'bank':
            if request.POST['item_name'] != '':
                temp_id = ""
                def id_gen(line):
                    count = 0
                    words = line.split(" ")
                    no_space = list(filter(None, words))
                    nick = ""
                    for i in line:
                        if (i.isspace()):
                            count = count + 1

                    for word in no_space:
                        nick += word[0].upper()

                    while sub_bank.objects.filter(sub_bank_id=nick):
                        nick += str(randint(1, 9))

                    return nick

                item = sub_bank()
                item.sub_bank_id = user_d.u_mc_id.mc_id + id_gen(request.POST['item_name'])
                item.sub_bank_name = request.POST['item_name']
                item.sub_bank_address = request.POST['item_address']
                item.sub_bank_tel = request.POST['item_tel']
                item.sub_bank_acc = request.POST['item_other']
                item.sub_mc_id = user_d.u_mc_id
                temp_id = item.sub_bank_id
                item.status = 1
                item.save()
                item = sub_bank.objects.get(sub_bank_id=temp_id)
                item_for_view.append({'id':item.sub_bank_id,'name':item.sub_bank_name, 'address':item.sub_bank_address, 'tele':item.sub_bank_tel, 'other':item.sub_bank_acc})
                str_slice = str(mc_id_len) + ":"
                return render(request, 'BPMS/manage_item.html',
                              {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                               'page_title': 'Bank Details',
                           'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice, 'th_id':'Bank ID',
                       'th_name':'Bank Name', 'th_address':'Bank Address', 'th_tel' : 'Contact Number',
                       'th_other':'Acc Number', 'frm_header':'Bank Details'})
            else:
                item_for_view.append({'id': '', 'name': '', 'address': '', 'tele': '', 'other': ''})
                str_slice = str(mc_id_len) + ":"
                return render(request, 'BPMS/manage_item.html',
                              {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                               'page_title': 'Add New Bank Acc',
                               'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                               'th_id': 'Bank ID',
                               'th_name': 'Bank Name', 'th_address': 'Bank Address', 'th_tel': 'Contact Number',
                               'th_other': 'Acc Number', 'frm_header': 'Bank Details'})

        elif request.POST.get('todo', '0') == 'add' and request.POST.get('item_type', '0') == 'client':
            if request.POST['item_name'] != '':
                temp_id = ""

                def id_gen(line):
                    count = 0
                    words = line.split(" ")
                    no_space = list(filter(None, words))
                    nick = ""
                    for i in line:
                        if (i.isspace()):
                            count = count + 1

                    for word in no_space:
                        nick += word[0].upper()

                    while sub_clients.objects.filter(sub_client_id=nick):
                        nick += str(randint(1, 9))

                    return nick

                item = sub_clients()
                item.sub_client_id = user_d.u_mc_id.mc_id + id_gen(request.POST['item_name'])
                item.sub_client_name = request.POST['item_name']
                item.sub_address = request.POST['item_address']
                item.sub_tele = request.POST['item_tel']
                item.sub_contact_person = request.POST['item_other']
                item.sub_mc_id = user_d.u_mc_id
                temp_id = item.sub_client_id
                item.status = 1
                item.save()
                item = sub_clients.objects.get(sub_client_id=temp_id)
                item_for_view.append(
                    {'id': item.sub_client_id, 'name': item.sub_client_name, 'address': item.sub_address,
                     'tele': item.sub_tele, 'other': item.sub_contact_person})
                str_slice = str(mc_id_len) + ":"
                return render(request, 'BPMS/manage_item.html',
                              {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                               'page_title': 'Client Details',
                               'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                               'th_id': 'Client ID',
                               'th_name': 'Client Name', 'th_address': 'Client Address', 'th_tel': 'Contact Number',
                               'th_other': 'Contact Person', 'frm_header': 'Client Details'})
            else:
                item_for_view.append({'id': '', 'name': '', 'address': '', 'tele': '', 'other': ''})
                str_slice = str(mc_id_len) + ":"
                return render(request, 'BPMS/manage_item.html',
                              {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                               'page_title': 'Add New Bank Acc',
                               'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                               'th_id': 'Bank ID',
                               'th_name': 'Bank Name', 'th_address': 'Bank Address', 'th_tel': 'Contact Number',
                               'th_other': 'Acc Number', 'frm_header': 'Bank Details'})


        elif request.POST.get('todo', '0') == 'delete' and request.POST.get('item_type', '0') == 'client':
            item = sub_clients.objects.get(sub_client_id=user_d.u_mc_id.mc_id + request.POST['item_id'])
            item.status = 0
            item.save()
            user_d = users.objects.get(u_user_id=request.session['u_name'])
            mc_id_len = len(user_d.u_mc_id.mc_id)
            item_data = sub_clients.objects.filter(Q(sub_mc_id=user_d.u_mc_id.mc_id), Q(status=1))
            item_for_view = []
            for item in item_data:
                item_for_view.append(
                    {'id': item.sub_client_id, 'name': item.sub_client_name, 'address': item.sub_address,
                     'tele': item.sub_tele, 'other': item.sub_contact_person})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_view.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']),
                           'page_title': 'View Clients',
                           'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                           'th_id': 'Client ID',
                           'th_name': 'Client Name', 'th_address': 'Client Address', 'th_tel': 'Contact Number',
                           'th_other': 'Contact Person', 'e': '1'})

        elif request.POST.get('todo', '0') == 'delete' and request.POST.get('item_type', '0') == 'bank':
            item = sub_bank.objects.get(sub_bank_id=user_d.u_mc_id.mc_id + request.POST['item_id'])
            item.status = 0
            item.save()

            user_d = users.objects.get(u_user_id=request.session['u_name'])
            mc_id_len = len(user_d.u_mc_id.mc_id)
            item_data = sub_bank.objects.filter(Q(sub_mc_id=user_d.u_mc_id.mc_id), Q(status=1))
            item_for_view = []
            for item in item_data:
                item_for_view.append(
                    {'id': item.sub_bank_id, 'name': item.sub_bank_name, 'address': item.sub_bank_address,
                     'tele': item.sub_bank_tel, 'other': item.sub_bank_acc})
            str_slice = str(mc_id_len) + ":"
            return render(request, 'BPMS/manage_view.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']), 'page_title': 'View Banks',
                           'item_data': item_for_view, 'mc_id_len': mc_id_len, 'str_slice': str_slice,
                           'th_id': 'Bank ID',
                           'th_name': 'Bank Name', 'th_address': 'Bank Address', 'th_tel': 'Contact Number',
                           'th_other': 'Acc Number', 'e': '2'})

