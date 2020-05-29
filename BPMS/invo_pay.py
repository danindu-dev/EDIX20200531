from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from collections import OrderedDict


def invo_settle(request):
    user_d = users.objects.get(u_user_id=request.session['u_name'])
    return render(request, 'BPMS/invo_pay.html', {'user_d':users.objects.get(u_user_id=request.session['u_name']), 'page_title':'Payment'})
