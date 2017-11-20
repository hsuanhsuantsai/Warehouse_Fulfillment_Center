from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class API(models.Model):
	api = models.CharField(max_length=50, primary_key=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.api

class Status(models.Model):
	description = models.CharField(max_length=100, primary_key=True)

	def __str__(self):
		return self.description
		
class Seller(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	sellerAPI = models.ForeignKey(API)
	endpoint = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_seller(sender, instance, created, **kwargs):
    if created:
    	api = str(uuid.uuid4())
    	try:
    		tmp = API.objects.get(pk=api)
    	except Exception as e:
    		tmp = None

    	while tmp is not None:
    		api = str(uuid.uuid4())
    		try:
    			tmp = API.objects.get(pk=api)
    		except Exception as e:
    			tmp = None
    		
    	tmp = API.objects.create(api=api)
    	Seller.objects.create(user=instance, sellerAPI=tmp)

@receiver(post_save, sender=User)
def save_user_seller(sender, instance, **kwargs):
    instance.seller.save()

class Item(models.Model):
	sku = models.CharField(max_length=100)
	sellerAPI = models.ForeignKey(API)
	quantity = models.IntegerField()
	status = models.ForeignKey(Status)
	shipping_address = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return self.sku

