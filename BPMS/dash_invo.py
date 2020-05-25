from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from collections import OrderedDict

def issue(request):
    if (request.method == "POST"):
        if request.POST['invoice_number'] and request.POST['invoice_date'] and request.POST['cid'] and request.POST['alltext'] and request.POST['allnum'] and request.POST['alltax'] and request.POST['g_total_to_submit'] and request.POST['invoice_due_date'] :
            user_d = users.objects.get(u_user_id=request.session['u_name'])
            new_invoice_reg = sub_credit_info()
            new_invoice_reg.c_invoice_num= user_d.u_mc_id.mc_id+request.POST['invoice_number']
            new_invoice_reg.c_invoice_date= request.POST['invoice_date']
            new_invoice_reg.sub_client_id = sub_clients.objects.get(sub_client_id=str(user_d.u_mc_id.mc_id+request.POST['cid'].upper()))
            new_invoice_reg.c_description = request.POST['alltext']
            new_invoice_reg.c_detail_amount = request.POST['allnum']
            new_invoice_reg.c_tax_string = request.POST['alltax']
            new_invoice_reg.c_total_amount = float(request.POST['g_total_to_submit'])
            new_invoice_reg.c_tax1_name=request.POST['tax_name']
            new_invoice_reg.c_tax1 = float(request.POST['tax_amount'])
            new_invoice_reg.c_discount = float(request.POST.get('deduction_value', '0'))
            new_invoice_reg.c_PO_num = request.POST.get('ponum', 'Not Available')
            new_invoice_reg.c_due_date = request.POST['invoice_due_date']
            new_invoice_reg.c_received_amount=0
            new_invoice_reg.c_received_date="1111-11-11"
            new_invoice_reg.sub_bank_id = sub_bank.objects.get(sub_bank_id="pending")
            new_invoice_reg.c_mc_id=user_d.u_mc_id
            new_invoice_reg.c_status="open"
            new_invoice_reg.save()
            update_mc = mc_details.objects.get(mc_id=user_d.u_mc_id.mc_id)
            update_mc.mc_lastinvoice = new_invoice_reg.c_invoice_num
            update_mc.save()
            return render(request, 'BPMS/new_invoice.html', {'user_d': users.objects.get(u_user_id=request.session['u_name']), 'page_title':'New Invoice', 'save': str(request.POST['invoice_number'])})
        else:
            return render(request, 'BPMS/new_invoice.html',
                      {'user_d': users.objects.get(u_user_id=request.session['u_name']),'page_title':'New Invoice', 'save': 'Incomplete!'})
    else:
        return render(request, 'BPMS/new_invoice.html',
                      {'user_d': users.objects.get(u_user_id=request.session['u_name']),'page_title':'New Invoice', 'save': 'not submited!'})



def new_invoice(request):
    user_d = users.objects.get(u_user_id=request.session['u_name'])
    sub_cid = sub_clients.objects.filter(sub_mc_id=user_d.u_mc_id.mc_id)
    mc_id_len = len(user_d.u_mc_id.mc_id)
    cid_list=[]
    cid_name=[]
    for cid in sub_cid:
        cid_list.append(cid.sub_client_id[mc_id_len:])
        cid_name.append(cid.sub_client_name)
    a= dict(zip(cid_list,cid_name))
    cid_comb = OrderedDict(sorted(a.items()))
    tax={'tax_name':sub_tax.objects.get(sub_mc_id=user_d.u_mc_id.mc_id).sub_tax_id[mc_id_len:] ,'tax_value':sub_tax.objects.get(sub_mc_id=user_d.u_mc_id.mc_id).sub_tax_amount, 'tax_default':sub_tax.objects.get(sub_mc_id=user_d.u_mc_id.mc_id).sub_tax_default}
    if user_d.u_mc_id.mc_lastinvoice != "":
        last_sub_credit_info = user_d.u_mc_id.mc_lastinvoice
        invo = last_sub_credit_info[mc_id_len:]
        to_invoice={}
        try:
            to_invoice['invo_num'] = int(invo)
            to_invoice['invo_num'] +=1
            to_invoice['invo_new_str'] = str(to_invoice['invo_num'])
            while len(to_invoice['invo_new_str']) < len(invo):
                to_invoice['invo_new_str'] = "0" + to_invoice['invo_new_str']

            return render(request, 'BPMS/new_invoice.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']),'page_title':'New Invoice', 'new_invoice': to_invoice['invo_new_str'], 'today':str(datetime.now().date()), 'due_date':str(datetime.now().date()+timedelta(days=30)), 'cid_comb':cid_comb, 'tax':tax})
        except ValueError:
            return render(request, 'BPMS/new_invoice.html',
                          {'user_d': users.objects.get(u_user_id=request.session['u_name']),'page_title':'New Invoice', 'today':str(datetime.now().date()), 'due_date':str(datetime.now().date()+timedelta(days=30)), 'cid_comb':cid_comb, 'tax':tax})

    else:
        return render(request, 'BPMS/new_invoice.html', {'user_d':users.objects.get(u_user_id=request.session['u_name']), 'page_title':'New Invoice', 'today':str(datetime.now().date()), 'due_date':str(datetime.now().date()+timedelta(days=30)), 'cid_comb':cid_comb, 'tax':tax})
    #return render(request, 'BPMS/new_invoice.html', {'user_d':users.objects.get(u_user_id=request.session['u_name'])})


def invo_view(request):
    user_d = users.objects.get(u_user_id=request.session['u_name'])
    mc_id_len = len(user_d.u_mc_id.mc_id)
    invo_edited=[]
    invo_data = sub_credit_info.objects.filter(c_mc_id=user_d.u_mc_id.mc_id)
    for item in invo_data:
        invo_edited.append(item.c_description.replace("?",","))
    invo_items = dict(zip(invo_data,invo_edited))
    str_slice=str(mc_id_len)+":"
    return render(request, 'BPMS/invo_view.html', {'user_d':users.objects.get(u_user_id=request.session['u_name']), 'page_title':'View Invoice', 'invo_items':invo_items, 'mc_id_len':mc_id_len,'str_slice':str_slice})

def invo_preview(request,invo_num):
    user_d = users.objects.get(u_user_id=request.session['u_name'])
    invo_data = sub_credit_info.objects.get(c_invoice_num=user_d.u_mc_id.mc_id+invo_num)
    mc_id_len = len(user_d.u_mc_id.mc_id)
    str_slice=str(mc_id_len)+":"

    line = invo_data.c_description
    words = line.split("?")
    no_space = list(filter(None, words))


    """invo_edited=[]
    invo_data = sub_credit_info.objects.filter(c_mc_id=user_d.u_mc_id.mc_id)
    for item in invo_data:
        invo_edited.append(item.c_description.replace("?",","))
    invo_items = dict(zip(invo_data,invo_edited))
    
    """
    return render(request, 'BPMS/invoice_preview.html', {'user_d':users.objects.get(u_user_id=request.session['u_name']),'no_space':no_space, 'str_slice':str_slice,'invo_data':invo_data})

def dashboard(request):
    return render(request, 'BPMS/dash.html', {'user_d':users.objects.get(u_user_id=request.session['u_name']), 'page_title':'Dashboard'})

def blank(request):
    return render(request, 'BPMS/blank_n.html', {'user_d':users.objects.get(u_user_id=request.session['u_name']), 'page_title':'Blank'})