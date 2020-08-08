from django.db import models
from accounts.models import Visitor, User
from campaign.models import Item

class Donation(models.Model):
    itemId = models.ForeignKey(Item, blank=False, null=True, on_delete=models.SET_NULL)
    donorUser = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    donorVisitor = models.ForeignKey(Visitor, blank=True, null=True, on_delete=models.SET_NULL)
    amount_payed = models.IntegerField( verbose_name="Donation")
    date_payed = models.DateTimeField( verbose_name="Transaction Date", auto_now_add=True)

    
    
