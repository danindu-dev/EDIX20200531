from django.db import models


class mc_details(models.Model):
    mc_id = models.CharField(max_length=10, primary_key=True)
    mc_name = models.CharField(max_length=250)
    mc_address = models.CharField(max_length=700)
    mc_email = models.CharField(max_length=100)
    mc_main_tele = models.CharField(max_length=15)
    mc_contact_person = models.CharField(max_length=100)
    mc_designation = models.CharField(max_length=100)
    mc_contact_person_mob = models.CharField(max_length=15)
    mc_registered_date = models.DateTimeField()
    mc_approved_by = models.CharField(max_length=10, blank=True, null=True)
    mc_approved_on = models.DateTimeField(blank=True, null=True)
    mc_num_sub_acc = models.IntegerField(blank=True, null=True)
    mc_currency = models.CharField(max_length=100)
    mc_lastinvoice = models.CharField(max_length=250)


class users(models.Model):
    u_user_id = models.CharField(max_length=250, primary_key=True)
    u_mc_id = models.ForeignKey(mc_details, on_delete=models.CASCADE)
    u_pwd = models.CharField(max_length=500)
    u_level = models.CharField(max_length=15)
    u_acc_status = models.CharField(max_length=15)




class sub_clients(models.Model):
    sub_client_id = models.CharField(max_length=15, primary_key=True)
    sub_client_name = models.CharField(max_length=250)
    sub_address = models.CharField(max_length=500)
    sub_tele = models.CharField(max_length=15)
    sub_contact_person = models.CharField(max_length=100)
    sub_mc_id = models.ForeignKey(mc_details, on_delete=models.CASCADE)
    status = models.BooleanField()


class sub_bank(models.Model):
    sub_bank_id = models.CharField(max_length=10, primary_key=True)
    sub_bank_name = models.CharField(max_length=100)
    sub_bank_address = models.CharField(max_length=700)
    sub_bank_tel = models.CharField(max_length=15)
    sub_bank_acc = models.CharField(max_length=100)
    sub_mc_id = models.ForeignKey(mc_details, on_delete=models.CASCADE)
    status = models.BooleanField()


class sub_credit_info(models.Model):
    c_invoice_num = models.CharField(max_length=100, primary_key=True)
    c_invoice_date = models.DateField()
    sub_client_id = models.ForeignKey(sub_clients, on_delete=models.CASCADE)
    c_description = models.TextField()
    c_detail_amount = models.TextField()
    c_total_amount = models.FloatField()
    c_received_amount = models.FloatField()
    c_received_date = models.DateField()
    c_cheque_num = models.CharField(max_length=25)
    c_remark = models.CharField(max_length=250)
    c_payment_type = models.CharField(max_length=10)
    sub_bank_id = models.ForeignKey(sub_bank, on_delete=models.CASCADE, default="NA")
    c_status = models.CharField(max_length=10, default="open")
    c_tax1_name = models.CharField(max_length=10)
    c_tax1 = models.FloatField(default=0)
    c_discount = models.FloatField(default=0)
    c_PO_num = models.CharField(max_length=100)
    c_note_to_client = models.TextField()
    c_mc_id = models.ForeignKey(mc_details, on_delete=models.CASCADE)
    c_tax_string = models.TextField()
    c_due_date = models.DateField()

class sub_tax(models.Model):
    sub_tax_id = models.CharField(max_length=100, primary_key=True)
    sub_tax_amount = models.FloatField(default=0)
    sub_tax_default = models.BooleanField()
    sub_mc_id = models.ForeignKey(mc_details, on_delete=models.CASCADE)


