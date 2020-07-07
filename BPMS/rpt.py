from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from collections import OrderedDict
from django.db.models import Q

def report_dash(request):
    return render(request, 'BPMS/report.html',
                  {'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')), 'page_title': 'Reports'})

def all_job_s(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    rpt_today = (datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))

    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['Client', 'Job Count', 'Net Amount', 'Discount', 'TAX Amount', 'Total with TAX', 'Received Amount','Due Amount']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo_oc = all_invo.filter(Q(c_status="open") | Q(c_status="close"))
        all_clients = sub_clients.objects.filter(sub_mc_id=user_d.u_mc_id)

        t_net_total = 0
        t_tax_total = 0
        t_grand_total = 0
        t_deduction = 0
        t_rcvd_amount = 0

        for client in all_clients:
            invos_for_client = all_invo_oc.filter(sub_client_id=client)
            net_total=0
            tax_total=0
            grand_total = 0
            deduction = 0
            rcvd_amount =0
            for invo_for_client in invos_for_client:
                amount_str = invo_for_client.c_detail_amount.split("?")
                amount_str = list(filter(None, amount_str))
                tax_str = invo_for_client.c_tax_string.split("?")
                tax_str = list(filter(None, tax_str))
                tax_amount = float(invo_for_client.c_tax1) * 0.01
                count = 0
                total = 0
                tax = 0
                for item_invo in amount_str:
                    total += float(item_invo)
                    if tax_str[count] == "add":
                        tax += (float(item_invo) * tax_amount)
                    count += 1
                net_total += total
                tax_total += tax
                grand_total += float(invo_for_client.c_total_amount)
                deduction += float(invo_for_client.c_discount)
                rcvd_amount += float(invo_for_client.c_received_amount)

            t_net_total += net_total
            t_tax_total += tax_total
            t_grand_total += grand_total
            t_deduction += deduction
            t_rcvd_amount += rcvd_amount


            client_temp = [client.sub_client_id[mc_id_len:],len(invos_for_client),"{:,.2f}".format(net_total),"{:,.2f}".format(deduction),"{:,.2f}".format(tax_total),"{:,.2f}".format(grand_total),"{:,.2f}".format(rcvd_amount),"{:,.2f}".format(grand_total-rcvd_amount)]
            td.append(client_temp)

        tdl = [' ',len(all_invo_oc),"{:,.2f}".format(t_net_total),"{:,.2f}".format(t_deduction),"{:,.2f}".format(t_tax_total),"{:,.2f}".format(t_grand_total),"{:,.2f}".format(t_rcvd_amount),"{:,.2f}".format(t_grand_total-t_rcvd_amount)]




    return render(request, 'BPMS/report_sum.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'cr':cr,'report_title':'Statement of All Invoices', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def unsettled_job_s(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['Client', 'Job Count', 'Net Amount', 'Discount', 'TAX Amount', 'Total with TAX', 'Received Amount','Due Amount']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        unstl_all_invo_not_date = all_invo_not_date.filter(c_status='open')
        all_invo = unstl_all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_clients = sub_clients.objects.filter(sub_mc_id=user_d.u_mc_id)

        t_net_total = 0
        t_tax_total = 0
        t_grand_total = 0
        t_deduction = 0
        t_rcvd_amount = 0

        for client in all_clients:
            invos_for_client = all_invo.filter(sub_client_id=client)
            net_total=0
            tax_total=0
            grand_total = 0
            deduction = 0
            rcvd_amount =0
            for invo_for_client in invos_for_client:
                amount_str = invo_for_client.c_detail_amount.split("?")
                amount_str = list(filter(None, amount_str))
                tax_str = invo_for_client.c_tax_string.split("?")
                tax_str = list(filter(None, tax_str))
                tax_amount = float(invo_for_client.c_tax1) * 0.01
                count = 0
                total = 0
                tax = 0
                for item_invo in amount_str:
                    total += float(item_invo)
                    if tax_str[count] == "add":
                        tax += (float(item_invo) * tax_amount)
                    count += 1
                net_total += total
                tax_total += tax
                grand_total += float(invo_for_client.c_total_amount)
                deduction += float(invo_for_client.c_discount)
                rcvd_amount += float(invo_for_client.c_received_amount)

            t_net_total += net_total
            t_tax_total += tax_total
            t_grand_total += grand_total
            t_deduction += deduction
            t_rcvd_amount += rcvd_amount


            client_temp = [client.sub_client_id[mc_id_len:],len(invos_for_client),"{:,.2f}".format(net_total),"{:,.2f}".format(deduction),"{:,.2f}".format(tax_total),"{:,.2f}".format(grand_total),"{:,.2f}".format(rcvd_amount),"{:,.2f}".format(grand_total-rcvd_amount)]
            td.append(client_temp)
        tdl = [' ', len(all_invo), "{:,.2f}".format(t_net_total), "{:,.2f}".format(t_deduction),
               "{:,.2f}".format(t_tax_total), "{:,.2f}".format(t_grand_total), "{:,.2f}".format(t_rcvd_amount),
               "{:,.2f}".format(t_grand_total - t_rcvd_amount)]




    return render(request, 'BPMS/report_sum.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'report_title':'Statement of Unsettled Invoices','tdl':tdl,'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def settled_job_s(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['Client', 'Job Count', 'Net Amount', 'Discount', 'TAX Amount', 'Total with TAX', 'Received Amount','Due Amount']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        unstl_all_invo_not_date = all_invo_not_date.filter(c_status='close')
        all_invo = unstl_all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_clients = sub_clients.objects.filter(sub_mc_id=user_d.u_mc_id)

        t_net_total = 0
        t_tax_total = 0
        t_grand_total = 0
        t_deduction = 0
        t_rcvd_amount = 0

        for client in all_clients:
            invos_for_client = all_invo.filter(sub_client_id=client)
            net_total=0
            tax_total=0
            grand_total = 0
            deduction = 0
            rcvd_amount =0
            for invo_for_client in invos_for_client:
                amount_str = invo_for_client.c_detail_amount.split("?")
                amount_str = list(filter(None, amount_str))
                tax_str = invo_for_client.c_tax_string.split("?")
                tax_str = list(filter(None, tax_str))
                tax_amount = float(invo_for_client.c_tax1) * 0.01
                count = 0
                total = 0
                tax = 0
                for item_invo in amount_str:
                    total += float(item_invo)
                    if tax_str[count] == "add":
                        tax += (float(item_invo) * tax_amount)
                    count += 1
                net_total += total
                tax_total += tax
                grand_total += float(invo_for_client.c_total_amount)
                deduction += float(invo_for_client.c_discount)
                rcvd_amount += float(invo_for_client.c_received_amount)

            t_net_total += net_total
            t_tax_total += tax_total
            t_grand_total += grand_total
            t_deduction += deduction
            t_rcvd_amount += rcvd_amount


            client_temp = [client.sub_client_id[mc_id_len:],len(invos_for_client),"{:,.2f}".format(net_total),"{:,.2f}".format(deduction),"{:,.2f}".format(tax_total),"{:,.2f}".format(grand_total),"{:,.2f}".format(rcvd_amount),"{:,.2f}".format(grand_total-rcvd_amount)]
            td.append(client_temp)
        tdl = [' ', len(all_invo), "{:,.2f}".format(t_net_total), "{:,.2f}".format(t_deduction),
               "{:,.2f}".format(t_tax_total), "{:,.2f}".format(t_grand_total), "{:,.2f}".format(t_rcvd_amount),
               "{:,.2f}".format(t_grand_total - t_rcvd_amount)]




    return render(request, 'BPMS/report_sum.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'report_title':'Statement of Settled Invoices','tdl':tdl,'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def all_job_d(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['#', 'Date', 'Invoice Number', 'Client', 'Description', 'Amount', 'Deductions', 'Tax','Total','Received','Due Amout','Rcvd Date','Chq No','Bank','Status']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo = all_invo.filter(Q(c_status = 'open') | Q(c_status = 'close'))

        t_net_total = 0
        t_tax_total = 0
        t_grand_total = 0
        t_deduction = 0
        t_rcvd_amount = 0

        invo_count = 1
        for invo_for_client in all_invo:
            grand_total = float(invo_for_client.c_total_amount)
            deduction = float(invo_for_client.c_discount)
            rcvd_amount = float(invo_for_client.c_received_amount)
            amount_str = invo_for_client.c_detail_amount.split("?")
            amount_str = list(filter(None, amount_str))
            tax_str = invo_for_client.c_tax_string.split("?")
            tax_str = list(filter(None, tax_str))
            tax_amount = float(invo_for_client.c_tax1) * 0.01
            count = 0
            total = 0
            tax = 0
            for item_invo in amount_str:
                total += float(item_invo)
                if tax_str[count] == "add":
                    tax += (float(item_invo) * tax_amount)
                count += 1
            client_temp = [invo_count, str(invo_for_client.c_invoice_date),
                           str(invo_for_client.c_invoice_num[mc_id_len:]),
                           str(invo_for_client.sub_client_id.sub_client_id[mc_id_len:]),
                           str(invo_for_client.c_description.replace('?', ',')[:-1]), "{:,.2f}".format(total),
                           "{:,.2f}".format(deduction), "{:,.2f}".format(tax), "{:,.2f}".format(grand_total),
                           "{:,.2f}".format(rcvd_amount), "{:,.2f}".format(grand_total - rcvd_amount),
                           str(invo_for_client.c_received_date), invo_for_client.c_cheque_num,
                           str(invo_for_client.sub_bank_id.sub_bank_id[mc_id_len:]), invo_for_client.c_status]
            td.append(client_temp)

            t_net_total += total
            t_tax_total += tax
            t_grand_total += grand_total
            t_deduction += deduction
            t_rcvd_amount += rcvd_amount
            invo_count += 1

        tdl = [' ',' ',' ',' ',' ',"{:,.2f}".format(t_net_total),"{:,.2f}".format(t_deduction),"{:,.2f}".format(t_tax_total),"{:,.2f}".format(t_grand_total),"{:,.2f}".format(t_rcvd_amount),"{:,.2f}".format(t_grand_total-t_rcvd_amount),' ',' ',' ',' ']

    return render(request, 'BPMS/report_details.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'report_title':' Detail Statement of All Invoices', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def unsettled_job_d(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['#', 'Date', 'Invoice Number', 'Client', 'Description', 'Amount', 'Deductions', 'Tax','Total','Received','Due Amout','Rcvd Date','Chq No','Bank','Status']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo = all_invo.filter(c_status = 'open')

        t_net_total = 0
        t_tax_total = 0
        t_grand_total = 0
        t_deduction = 0
        t_rcvd_amount = 0

        invo_count = 1
        for invo_for_client in all_invo:
            grand_total = float(invo_for_client.c_total_amount)
            deduction = float(invo_for_client.c_discount)
            rcvd_amount = float(invo_for_client.c_received_amount)
            amount_str = invo_for_client.c_detail_amount.split("?")
            amount_str = list(filter(None, amount_str))
            tax_str = invo_for_client.c_tax_string.split("?")
            tax_str = list(filter(None, tax_str))
            tax_amount = float(invo_for_client.c_tax1) * 0.01
            count = 0
            total = 0
            tax = 0
            for item_invo in amount_str:
                total += float(item_invo)
                if tax_str[count] == "add":
                    tax += (float(item_invo) * tax_amount)
                count += 1
            client_temp = [invo_count, str(invo_for_client.c_invoice_date),
                           str(invo_for_client.c_invoice_num[mc_id_len:]),
                           str(invo_for_client.sub_client_id.sub_client_id[mc_id_len:]),
                           str(invo_for_client.c_description.replace('?', ',')[:-1]), "{:,.2f}".format(total),
                           "{:,.2f}".format(deduction), "{:,.2f}".format(tax), "{:,.2f}".format(grand_total),
                           "{:,.2f}".format(rcvd_amount), "{:,.2f}".format(grand_total - rcvd_amount),
                           str(invo_for_client.c_received_date), invo_for_client.c_cheque_num,
                           str(invo_for_client.sub_bank_id.sub_bank_id[mc_id_len:]), invo_for_client.c_status]
            td.append(client_temp)

            t_net_total += total
            t_tax_total += tax
            t_grand_total += grand_total
            t_deduction += deduction
            t_rcvd_amount += rcvd_amount
            invo_count += 1

        tdl = [' ',' ',' ',' ',' ',"{:,.2f}".format(t_net_total),"{:,.2f}".format(t_deduction),"{:,.2f}".format(t_tax_total),"{:,.2f}".format(t_grand_total),"{:,.2f}".format(t_rcvd_amount),"{:,.2f}".format(t_grand_total-t_rcvd_amount),' ',' ',' ',' ']

    return render(request, 'BPMS/report_details.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'report_title':'Detail Statement of Unsettled Invoices', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def settled_job_d(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['#', 'Date', 'Invoice Number', 'Client', 'Description', 'Amount', 'Deductions', 'Tax','Total','Received','Due Amout','Rcvd Date','Chq No','Bank','Status']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo = all_invo.filter(c_status = 'close')

        t_net_total = 0
        t_tax_total = 0
        t_grand_total = 0
        t_deduction = 0
        t_rcvd_amount = 0

        invo_count = 1
        for invo_for_client in all_invo:
            grand_total = float(invo_for_client.c_total_amount)
            deduction = float(invo_for_client.c_discount)
            rcvd_amount = float(invo_for_client.c_received_amount)
            amount_str = invo_for_client.c_detail_amount.split("?")
            amount_str = list(filter(None, amount_str))
            tax_str = invo_for_client.c_tax_string.split("?")
            tax_str = list(filter(None, tax_str))
            tax_amount = float(invo_for_client.c_tax1) * 0.01
            count = 0
            total = 0
            tax = 0
            for item_invo in amount_str:
                total += float(item_invo)
                if tax_str[count] == "add":
                    tax += (float(item_invo) * tax_amount)
                count += 1
            client_temp = [invo_count, str(invo_for_client.c_invoice_date),
                           str(invo_for_client.c_invoice_num[mc_id_len:]),
                           str(invo_for_client.sub_client_id.sub_client_id[mc_id_len:]),
                           str(invo_for_client.c_description.replace('?', ',')[:-1]), "{:,.2f}".format(total),
                           "{:,.2f}".format(deduction), "{:,.2f}".format(tax), "{:,.2f}".format(grand_total),
                           "{:,.2f}".format(rcvd_amount), "{:,.2f}".format(grand_total - rcvd_amount),
                           str(invo_for_client.c_received_date), invo_for_client.c_cheque_num,
                           str(invo_for_client.sub_bank_id.sub_bank_id[mc_id_len:]), invo_for_client.c_status]
            td.append(client_temp)

            t_net_total += total
            t_tax_total += tax
            t_grand_total += grand_total
            t_deduction += deduction
            t_rcvd_amount += rcvd_amount
            invo_count += 1

        tdl = [' ',' ',' ',' ',' ',"{:,.2f}".format(t_net_total),"{:,.2f}".format(t_deduction),"{:,.2f}".format(t_tax_total),"{:,.2f}".format(t_grand_total),"{:,.2f}".format(t_rcvd_amount),"{:,.2f}".format(t_grand_total-t_rcvd_amount),' ',' ',' ',' ']

    return render(request, 'BPMS/report_details.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'report_title':'Detail Statement of Settled Invoices', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def cr(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    crd = datetime.now().date() + timedelta(days=15)
    rpt_today = datetime.now().date()
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['Date', 'Invoice Number','Description', 'Net Amount', 'Discount', 'TAX Amount', 'Total with TAX', 'Received Amount','Due Amount']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo_oc = all_invo.filter(c_status="open")
        all_clients = sub_clients.objects.filter(sub_mc_id=user_d.u_mc_id)


        for client in all_clients:
            invos_for_client = all_invo_oc.filter(sub_client_id=client)
            if len(invos_for_client) != 0 :
                ctd = []
                net_total=0
                tax_total=0
                grand_total = 0
                deduction = 0
                rcvd_amount =0
                for invo_for_client in invos_for_client:
                    amount_str = invo_for_client.c_detail_amount.split("?")
                    amount_str = list(filter(None, amount_str))
                    tax_str = invo_for_client.c_tax_string.split("?")
                    tax_str = list(filter(None, tax_str))
                    tax_amount = float(invo_for_client.c_tax1) * 0.01
                    count = 0
                    total = 0
                    tax = 0
                    rcvd_amount_i = 0
                    deduction_i = 0
                    for item_invo in amount_str:
                        total += float(item_invo)
                        if tax_str[count] == "add":
                            tax += (float(item_invo) * tax_amount)
                        count += 1
                    net_total += total
                    tax_total += tax
                    grand_total += float(invo_for_client.c_total_amount)
                    deduction_i += float(invo_for_client.c_discount)
                    rcvd_amount_i += float(invo_for_client.c_received_amount)
                    deduction += deduction_i
                    rcvd_amount += rcvd_amount_i
                    desc=str(invo_for_client.c_description.replace('?', ', ')[:-2])
                    ctd_temp = [str(invo_for_client.c_invoice_date), str(invo_for_client.c_invoice_num[mc_id_len:]), desc, "{:,.2f}".format(total),
                               "{:,.2f}".format(deduction_i), "{:,.2f}".format(tax), "{:,.2f}".format(float(invo_for_client.c_total_amount)),
                               "{:,.2f}".format(rcvd_amount_i), "{:,.2f}".format(float(invo_for_client.c_total_amount) - rcvd_amount_i)]
                    ctd.append(ctd_temp)

                ctd_temp = ['', '', '', '',
                               '', '', '',
                               '', "{:,.2f}".format(grand_total - rcvd_amount)]
                ctd.append(ctd_temp)
                client_temp = {client:ctd}
                td.append(client_temp)
                '''tdl ='''

    return render(request, 'BPMS/report_cr.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'crd':crd,'report_title':'Credit Notice', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def client_wise_unsettled(request):

    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th=[]
    td=[]
    tdl=[]
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    crd = str(datetime.now().date() + timedelta(days=15))
    rpt_today = datetime.now().date()
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['#','Date', 'Invoice Number','Client','Description', 'Net Amount', 'Discount', 'TAX Amount', 'Total with TAX', 'Received Amount','Due Amount','Status']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id = user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo_oc = all_invo.filter(c_status="open")
        all_clients = sub_clients.objects.filter(sub_mc_id=user_d.u_mc_id)


        for client in all_clients:
            invos_for_client = all_invo_oc.filter(sub_client_id=client)
            if len(invos_for_client) != 0 :
                ctd = []
                net_total=0
                tax_total=0
                grand_total = 0
                deduction = 0
                rcvd_amount =0
                invo_count=0
                for invo_for_client in invos_for_client:
                    amount_str = invo_for_client.c_detail_amount.split("?")
                    amount_str = list(filter(None, amount_str))
                    tax_str = invo_for_client.c_tax_string.split("?")
                    tax_str = list(filter(None, tax_str))
                    tax_amount = float(invo_for_client.c_tax1) * 0.01
                    invo_count += 1
                    count = 0
                    total = 0
                    tax = 0
                    rcvd_amount_i = 0
                    deduction_i = 0
                    for item_invo in amount_str:
                        total += float(item_invo)
                        if tax_str[count] == "add":
                            tax += (float(item_invo) * tax_amount)
                        count += 1
                    net_total += total
                    tax_total += tax
                    grand_total += float(invo_for_client.c_total_amount)
                    deduction_i += float(invo_for_client.c_discount)
                    rcvd_amount_i += float(invo_for_client.c_received_amount)
                    deduction += deduction_i
                    rcvd_amount += rcvd_amount_i
                    desc=str(invo_for_client.c_description.replace('?', ',')[:-1])
                    ctd_temp = [invo_count, str(invo_for_client.c_invoice_date), str(invo_for_client.c_invoice_num[mc_id_len:]), str(invo_for_client.sub_client_id.sub_client_id[mc_id_len:]), desc, "{:,.2f}".format(total),
                               "{:,.2f}".format(deduction_i), "{:,.2f}".format(tax), "{:,.2f}".format(float(invo_for_client.c_total_amount)),
                               "{:,.2f}".format(rcvd_amount_i), "{:,.2f}".format(float(invo_for_client.c_total_amount) - rcvd_amount_i),"OPEN"]
                    ctd.append(ctd_temp)

                ctd_temp = ['','','', '', '', "{:,.2f}".format(net_total),
                               "{:,.2f}".format(deduction), "{:,.2f}".format(tax_total),  "{:,.2f}".format(grand_total),
                               "{:,.2f}".format(rcvd_amount), "{:,.2f}".format(grand_total - rcvd_amount),'']
                ctd.append(ctd_temp)
                client_temp = {client:ctd}
                td.append(client_temp)
                '''tdl ='''

    return render(request, 'BPMS/report_cr.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'crd':crd,'report_title':'Client-wise - Detailed Report of Unsettled', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def client_wise_settled(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th = []
    td = []
    tdl = []
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    crd = str(datetime.now().date() + timedelta(days=15))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['#', 'Date', 'Invoice Number', 'Client', 'Description', 'Net Amount', 'Discount', 'TAX Amount',
              'Total with TAX', 'Received Amount', 'Due Amount', 'Status']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id=user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(
            c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo_oc = all_invo.filter(c_status="close")
        all_clients = sub_clients.objects.filter(sub_mc_id=user_d.u_mc_id)

        for client in all_clients:
            invos_for_client = all_invo_oc.filter(sub_client_id=client)
            if len(invos_for_client) != 0:
                ctd = []
                net_total = 0
                tax_total = 0
                grand_total = 0
                deduction = 0
                rcvd_amount = 0
                invo_count = 0
                for invo_for_client in invos_for_client:
                    amount_str = invo_for_client.c_detail_amount.split("?")
                    amount_str = list(filter(None, amount_str))
                    tax_str = invo_for_client.c_tax_string.split("?")
                    tax_str = list(filter(None, tax_str))
                    tax_amount = float(invo_for_client.c_tax1) * 0.01
                    invo_count += 1
                    count = 0
                    total = 0
                    tax = 0
                    rcvd_amount_i = 0
                    deduction_i = 0
                    for item_invo in amount_str:
                        total += float(item_invo)
                        if tax_str[count] == "add":
                            tax += (float(item_invo) * tax_amount)
                        count += 1
                    net_total += total
                    tax_total += tax
                    grand_total += float(invo_for_client.c_total_amount)
                    deduction_i += float(invo_for_client.c_discount)
                    rcvd_amount_i += float(invo_for_client.c_received_amount)
                    deduction += deduction_i
                    rcvd_amount += rcvd_amount_i
                    desc = str(invo_for_client.c_description.replace('?', ',')[:-1])
                    ctd_temp = [invo_count, str(invo_for_client.c_invoice_date),
                                str(invo_for_client.c_invoice_num[mc_id_len:]),
                                str(invo_for_client.sub_client_id.sub_client_id[mc_id_len:]), desc,
                                "{:,.2f}".format(total),
                                "{:,.2f}".format(deduction_i), "{:,.2f}".format(tax),
                                "{:,.2f}".format(float(invo_for_client.c_total_amount)),
                                "{:,.2f}".format(rcvd_amount_i),
                                "{:,.2f}".format(float(invo_for_client.c_total_amount) - rcvd_amount_i), "CLOSED"]
                    ctd.append(ctd_temp)

                ctd_temp = ['', '', '', '', '', "{:,.2f}".format(net_total),
                            "{:,.2f}".format(deduction), "{:,.2f}".format(tax_total), "{:,.2f}".format(grand_total),
                            "{:,.2f}".format(rcvd_amount), "{:,.2f}".format(grand_total - rcvd_amount), '']
                ctd.append(ctd_temp)
                client_temp = {client: ctd}
                td.append(client_temp)
                '''tdl ='''


    return render(request, 'BPMS/report_cr.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'crd':crd,'report_title':'Client-wise - Detailed Report of Settled', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})


def bank_summary(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th = []
    td = []
    tdl = []
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['Count', 'Received Amount']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id=user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(
            c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo_oc = all_invo.filter(c_payment_type="BANK")
        all_banks = sub_bank.objects.filter(sub_mc_id=user_d.u_mc_id)

        for client in all_banks:
            invos_for_client = all_invo_oc.filter(sub_bank_id=client)
            if len(invos_for_client) != 0:
                ctd = []
                rcvd_amount = 0
                invo_count = 0
                for invo_for_client in invos_for_client:
                    invo_count += 1
                    rcvd_amount += float(invo_for_client.c_received_amount)
                ctd_temp = [invo_count, "{:,.2f}".format(rcvd_amount)]
                ctd_temp1 = ['', '']
                ctd.append(ctd_temp)
                ctd.append(ctd_temp1)
                client_temp = {client: ctd}
                td.append(client_temp)


    return render(request, 'BPMS/report_bank_s.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'report_title':'Bank Summary Statement', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})


def bank_statement(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    mc_id_len = len(user_d.u_mc_id.mc_id)
    th = []
    td = []
    tdl = []
    stat = '0'
    today = str(datetime.now().date())
    from_date = str(datetime.now().date() - timedelta(days=18250))
    rpt_today = (datetime.now().date())
    if (request.method == "POST"):
        stat = '1'
        today = request.POST['report_to_d']
        from_date = request.POST['report_from_d']
        th = ['#', 'Date', 'Invoice Number', 'Client', 'Description', 'Net Amount', 'Discount', 'TAX Amount',
              'Total with TAX', 'Received Amount', 'Due Amount', 'Status']
        all_invo_not_date = sub_credit_info.objects.filter(c_mc_id=user_d.u_mc_id).order_by('-c_invoice_date')
        all_invo = all_invo_not_date.filter(
            c_invoice_date__range=[request.POST['report_from_d'], request.POST['report_to_d']])
        all_invo_oc = all_invo.filter(c_payment_type="BANK")
        all_banks = sub_bank.objects.filter(sub_mc_id=user_d.u_mc_id)

        for client in all_banks:
            invos_for_client = all_invo_oc.filter(sub_bank_id=client)
            if len(invos_for_client) != 0:
                ctd = []
                net_total = 0
                tax_total = 0
                grand_total = 0
                deduction = 0
                rcvd_amount = 0
                invo_count = 0
                for invo_for_client in invos_for_client:
                    amount_str = invo_for_client.c_detail_amount.split("?")
                    amount_str = list(filter(None, amount_str))
                    tax_str = invo_for_client.c_tax_string.split("?")
                    tax_str = list(filter(None, tax_str))
                    tax_amount = float(invo_for_client.c_tax1) * 0.01
                    invo_count += 1
                    count = 0
                    total = 0
                    tax = 0
                    rcvd_amount_i = 0
                    deduction_i = 0
                    for item_invo in amount_str:
                        total += float(item_invo)
                        if tax_str[count] == "add":
                            tax += (float(item_invo) * tax_amount)
                        count += 1
                    net_total += total
                    tax_total += tax
                    grand_total += float(invo_for_client.c_total_amount)
                    deduction_i += float(invo_for_client.c_discount)
                    rcvd_amount_i += float(invo_for_client.c_received_amount)
                    deduction += deduction_i
                    rcvd_amount += rcvd_amount_i
                    desc = str(invo_for_client.c_description.replace('?', ',')[:-1])
                    ctd_temp = [invo_count, str(invo_for_client.c_invoice_date),
                                str(invo_for_client.c_invoice_num[mc_id_len:]),
                                str(invo_for_client.sub_client_id.sub_client_id[mc_id_len:]), desc,
                                "{:,.2f}".format(total),
                                "{:,.2f}".format(deduction_i), "{:,.2f}".format(tax),
                                "{:,.2f}".format(float(invo_for_client.c_total_amount)),
                                "{:,.2f}".format(rcvd_amount_i),
                                "{:,.2f}".format(float(invo_for_client.c_total_amount) - rcvd_amount_i), invo_for_client.c_status.upper()]
                    ctd.append(ctd_temp)

                ctd_temp = ['', '', '', '', '', "{:,.2f}".format(net_total),
                            "{:,.2f}".format(deduction), "{:,.2f}".format(tax_total), "{:,.2f}".format(grand_total),
                            "{:,.2f}".format(rcvd_amount), "{:,.2f}".format(grand_total - rcvd_amount), '']
                ctd.append(ctd_temp)
                client_temp = {client: ctd}
                td.append(client_temp)
                '''tdl ='''


    return render(request, 'BPMS/report_bank_s.html', {'rpt_today':rpt_today, 'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'report_title':'Bank Statement', 'tdl':tdl, 'th':th, 'td':td ,'stat':stat, 'page_title':'Reports','today':today, 'from_date':from_date})

def temp(request):
    user_d = users.objects.get(u_user_id=request.session.get('u_name','ALL'))
    th = ['a1','a1','a1','a1','a1','a1']
    td = [['b1','b1','b1','b1','b1','b1'], ['c1','c1','c1','c1','c1','c1']]

    return render(request, 'BPMS/report_temp.html', {'user_d':users.objects.get(u_user_id=request.session.get('u_name','ALL')),'th':th, 'td':td , 'page_title':'Reports','today':str(datetime.now().date()), 'from_date':str(datetime.now().date()-timedelta(days=30))})
