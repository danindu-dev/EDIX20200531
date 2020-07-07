from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from collections import OrderedDict
from django.db.models import Q


def invo_settle(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    if (request.method == "POST"):
        if (sub_credit_info.objects.filter(c_invoice_num=user_d.u_mc_id.mc_id + request.POST['invoice_num'])):
            if sub_credit_info.objects.get(c_invoice_num=user_d.u_mc_id.mc_id + request.POST['invoice_num']).c_status == "open" or request.POST.get('e_pay', '0') == '1':
                mc_id_len = len(user_d.u_mc_id.mc_id)
                str_slice = str(mc_id_len) + ":"
                invo_d=sub_credit_info.objects.get(c_invoice_num=user_d.u_mc_id.mc_id + request.POST['invoice_num'])
                invo_d.c_description = invo_d.c_description.replace("?", ", ")
                amount_str = invo_d.c_detail_amount.split("?")
                amount_str = list(filter(None, amount_str))
                tax_str = invo_d.c_tax_string.split("?")
                tax_str = list(filter(None, tax_str))
                tax_amount = float(invo_d.c_tax1)*0.01
                count = 0
                total = 0
                tax = 0
                for item in amount_str:
                    total += float(item)
                    if tax_str[count] == "add":
                        tax += (float(item)*tax_amount)
                    count += 1
                bank_data = sub_bank.objects.filter(sub_mc_id=user_d.u_mc_id.mc_id)
                return render(request, 'BPMS/invo_pay.html',{'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'bank_data' : bank_data,'total':total, 'tax':tax, 'str_slice': str_slice, 'today':str(datetime.now().date()), 'invo_d':invo_d, 'page_title': 'Payment','q': '0'})
            else:
                return render(request, 'BPMS/invo_pay.html',{'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'page_title': 'Payment','q': '1'})
        else:
            return render(request, 'BPMS/invo_pay.html',{'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'page_title': 'Payment','q': '1'})
    else:
        return render(request, 'BPMS/invo_pay.html', {'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'page_title':'Payment', 'q':'0'})


def invo_settle_conf(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    if (request.method == "POST"):
        if (sub_credit_info.objects.filter(c_invoice_num=user_d.u_mc_id.mc_id + request.POST['invo_num_conf'])):
            pay_update_d = sub_credit_info.objects.get(c_invoice_num=user_d.u_mc_id.mc_id + request.POST['invo_num_conf'])

            if request.POST['status_s'] == "CLOSE":
                pay_update_d.c_received_date = request.POST['received_date']
                pay_update_d.c_received_amount = float(request.POST['received_amount'])
                if (float(pay_update_d.c_total_amount)-float(request.POST['received_amount'])) != 0:
                    pay_update_d.c_status = 'open'
                else:
                    pay_update_d.c_status = 'close'

                if request.POST['remark'] != "":
                    pay_update_d.c_remark = request.POST['remark']
                if request.POST['bank'] == "CASH":
                    pay_update_d.c_payment_type = 'CASH'
                    pay_update_d.sub_bank_id = sub_bank.objects.get(sub_bank_id='done')
                else:
                    pay_update_d.c_payment_type = 'BANK'
                    pay_update_d.c_cheque_num = request.POST['che_num']
                    pay_update_d.sub_bank_id = sub_bank.objects.get(sub_bank_id=user_d.u_mc_id.mc_id + request.POST['bank'])
            elif request.POST['status_s'] == "CANCEL":
                pay_update_d.c_received_date = request.POST['received_date']
                pay_update_d.c_status = 'cancel'
            else:
                pay_update_d.c_received_date = '1111-11-11'
                pay_update_d.c_received_amount = 0
                pay_update_d.c_status = 'open'
                pay_update_d.c_remark = ""
                pay_update_d.c_payment_type = ''
                pay_update_d.sub_bank_id = sub_bank.objects.get(sub_bank_id='pending')
                pay_update_d.c_cheque_num = ''

            pay_update_d.save()
            return render(request, 'BPMS/invo_pay.html',{'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'page_title': 'Payment','q': '0', 'saved': str(request.POST['invo_num_conf'])})
        else:
            return render(request, 'BPMS/invo_pay.html',{'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'page_title': 'Payment','q': '0'})
    else:
        return render(request, 'BPMS/invo_pay.html', {'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'page_title': 'Payment', 'q': '1'})


def invo_settle_view(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    invo_edited=[]
    invo_data = sub_credit_info.objects.none()
    search_sub = ""
    if (request.method == "POST"):
        search_sub = "done"
        invo_data_temp = sub_credit_info.objects.filter(c_mc_id=user_d.u_mc_id.mc_id).order_by('-c_invoice_date')
        invo_data = invo_data_temp.filter(Q(c_invoice_num__icontains=request.POST.get('search-box', '')) | Q(
            c_description__icontains=request.POST.get('search-box', '')) | Q(
            c_invoice_date__icontains=request.POST.get('search-box', '')) | Q(
            c_total_amount__icontains=request.POST.get('search-box', '')) | Q(
            c_status__icontains=request.POST.get('search-box', '')) | Q(
            c_received_amount__icontains=request.POST.get('search-box', '')) | Q(
            c_received_date__icontains=request.POST.get('search-box', '')) | Q(
            c_cheque_num__icontains=request.POST.get('search-box', '')) | Q(
            c_payment_type__icontains=request.POST.get('search-box', ''))| Q(
            sub_client_id=sub_clients.objects.filter(sub_client_id=user_d.u_mc_id.mc_id+request.POST.get('search-box', '324df'))[:1]) | Q(
            c_PO_num__icontains=request.POST.get('search-box', '')))
    else:
        invo_data = sub_credit_info.objects.filter(c_mc_id=user_d.u_mc_id.mc_id).order_by('-c_invoice_date')[:50]
    for item in invo_data:
        invo_edited.append(item.c_description.replace("?",", "))
        item.c_received_amount = -1*item.c_received_amount
    invo_items = dict(zip(invo_data,invo_edited))
    str_slice=str(mc_id_len)+":"

    return render(request, 'BPMS/invo_pay_view.html', {'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'search_sub':search_sub, 'page_title':'View Payments', 'invo_items':invo_items, 'mc_id_len':mc_id_len,'str_slice':str_slice})
