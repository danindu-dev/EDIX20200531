"""EDIX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import lrf, invo_pay, dash_invo

urlpatterns = [
    path('login/', lrf.login),
    path('', lrf.login, name = 'login'),
    path('verify/', lrf.login_verify, name = 'verify'),
    path('signup/', lrf.signup, name = 'signup'),
    path('forapproval/', lrf.forapproval, name = 'forapproval'),
    path('dashboard/', dash_invo.dashboard, name = 'dashboard'),
    path('blank/', dash_invo.blank, name = 'blank'),
    path('new_invoice/', dash_invo.new_invoice, name = 'new_invoice'),
    path('new_invoice/issue', dash_invo.issue, name = 'new_invoice_issue'),
    path('invoice/', dash_invo.invo_view, name = 'invoice_view'),
    path('invoice/<str:invo_num>', dash_invo.invo_preview, name = 'invo_preview'),
    path('invoice/e/', dash_invo.invo_edit_update, name = 'invo_edit_update'),
    path('invoice/e/<str:invo_num>', dash_invo.invo_edit, name = 'invo_edit'),
    path('invoice/d/', dash_invo.invo_del, name = 'invo_del'),
    path('invoice/settle', invo_pay.invo_settle, name = 'invo_settle'),
]
