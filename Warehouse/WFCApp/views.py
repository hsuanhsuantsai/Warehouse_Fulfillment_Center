from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import auth
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from social_django.models import UserSocialAuth
import json
import requests
from django.views.decorators.csrf import csrf_exempt

def home(request):
	return render(request, 'home.html')

def QuickStart(request):
	return render(request, 'quickStart.html')

def documentation(request):
	return render(request, 'documentation.html')

# redirect to home after logout
def logout(request):
	auth.logout(request)
	return redirect(home)

def register(request):
	if request.user.is_authenticated() and request.user.is_active:
		return redirect(home)

	if request.method == 'GET':
		return render(request, 'register.html')
	elif request.method == 'POST':
		username = request.POST.get('username', '').strip()
		try:
			# check if the username has already registered
			# if not, the function throws an exception
			print(username)
			exist = User.objects.get(username=username)
			msg = 'Username is used, please choose another username'
			return render(request, 'Error.html', {'msg': msg})
		except Exception as e:
			password = request.POST.get('password', '').strip()
			first = request.POST.get('FirstName', '').strip()
			last = request.POST.get('LastName', '').strip()
			endpoint = request.POST.get('endpoint', '').strip()
			User.objects.create_user(username=username, password=password, 
				first_name=first, last_name=last)
			user = User.objects.get(username=username)
			seller = user.seller
			seller.endpoint = endpoint
			seller.save()
			return redirect('login')

	msg = 'Oops, something went wrong. Please try again later.'
	return render(request, 'Error.html', {'msg': msg})

@login_required
def settings(request):
	user = request.user

	if request.method == 'POST':
		endpoint = request.POST.get('new_endpoint', '').strip()
		seller = user.seller
		print(seller.endpoint)
		seller.endpoint = endpoint
		seller.save()
		print(seller.endpoint)
		return redirect(settings)

	try:
		github = user.social_auth.get(provider='github')
	except UserSocialAuth.DoesNotExist:
		github = None

	try:
		twitter = user.social_auth.get(provider='twitter')
	except UserSocialAuth.DoesNotExist:
		twitter = None

	# disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
	return render(request, 'settings.html', {'endpoint': user.seller.endpoint,
											# 'disconnect': disconnect,
											'github': github,
											'twitter': twitter})

@login_required
def password(request):
	if request.user.has_usable_password():
		password_form = PasswordChangeForm
	else:
		password_form = AdminPasswordChangeForm

	if request.method == 'POST':
		form = password_form(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return render(request, 'password.html', {'form': form,
													'success': True})
			# return redirect(password)
		else:
			return render(request, 'password.html', {'form': form,
													'success': False})
	else:
		form = password_form(request.user)

	return render(request, 'password.html', {'form': form,
											'success': False})

@login_required
def deleteAccount(request):
	print(request.user.username)
	if request.method == 'GET':
		return render(request, 'Delete.html')
	elif request.method == 'POST':
		username = request.user.username
		user = User.objects.get(username=username)
		api = user.seller.sellerAPI
		api.active = False
		api.save()
		# delete items related to this api
		Item.objects.filter(sellerAPI=api).delete()
		user.delete()
		print(username + ' is deleted!')
		return redirect(home)

	msg = 'Oops, something went wrong. Please try again later.'
	return render(request, 'ERROR.html', {'msg': msg})

@csrf_exempt
def inventory(request, api):
	try:
		api_obj = API.objects.get(api=api)
	except Exception as e:
		return JsonResponse({'Message': 'Invalid API!'}, status=400)

	if api_obj.active:
		if request.method == 'GET':
			items = serializers.serialize("json", Item.objects.filter(sellerAPI=api_obj))
			
			# Only return fields data
			tmp = json.loads(items)
			res = []
			for obj in tmp:
				obj_fields = obj['fields']
				del obj_fields['sellerAPI']
				del obj_fields['shipping_address']
				res.append(obj_fields)
			return HttpResponse(json.dumps(res), content_type='application/json')
		elif request.method == 'POST':
			body_unicode = request.body.decode('utf-8')
			# print(body_unicode)
			if body_unicode == '' or body_unicode == '[]':
				return JsonResponse({'Message': 'Please provide at least one item for replenishment!'}, status=400)
			
			body = json.loads(body_unicode)
			if len(body) > 100:
				return JsonResponse({'Message': 'Please provide at most 100 items each time!'}, status=400)

			flag = False
			for i in range(len(body)):
				r = replenish(i, body[i], api_obj)
				flag = flag or r

			if flag:
				return JsonResponse({'Message': 'Item replenishment done'})
			else:
				return JsonResponse({'Message': 'Invalid quantity in replenishments'}, status=400)

			return JsonResponse({'Message': 'Bad Request'}, status=400)

	return JsonResponse({'Message': 'Invalid API!'}, status=400)

def replenish(i, content, api_obj):
	sku = content['sku']
	try:
		qty = int(content['quantity'])
		print(qty)
		if qty < 0:
			print('qty < 0')
			return False
	except Exception as e:
		print('qty error')
		return False

	status = Status.objects.get(description='In Stock')
	items = Item.objects.filter(sellerAPI=api_obj).filter(sku=sku).filter(status=status)
	if len(items) == 0:
		Item.objects.create(sku=sku, sellerAPI=api_obj, quantity=qty, status=status)
	else:
		item_obj = items[0]
		item_obj.quantity += qty
		item_obj.save()

	return True

def item(request, api, sku):
	if request.method != 'GET':
		return HttpResponseBadRequest()
	try:
		api_obj = API.objects.get(api=api)
	except Exception as e:
		return JsonResponse({'Message': 'Invalid API!'}, status=400)

	if api_obj.active:
		items = serializers.serialize("json", Item.objects.filter(sellerAPI=api_obj).filter(sku=sku))
		tmp = json.loads(items)
		res = []
		for obj in tmp:
			obj_fields = obj['fields']
			del obj_fields['sellerAPI']
			del obj_fields['shipping_address']
			res.append(obj_fields)
		return HttpResponse(json.dumps(res), content_type='application/json')
	return JsonResponse({'Message': 'Invalid API!'}, status=400)

@csrf_exempt
def orders(request, api):
	try:
		api_obj = API.objects.get(api=api)
	except Exception as e:
		return JsonResponse({'Message': 'Invalid API!'}, status=400)

	if api_obj.active:
		if request.method == 'POST':
			# type(body_unicode): str
			body_unicode = request.body.decode('utf-8')
			if body_unicode == '' or body_unicode == '[]':
				return JsonResponse({'Message': 'Please provide at least one item for order placement!'}, status=400)
			body = json.loads(body_unicode)
			if len(body) > 100:
				return JsonResponse({'Message': 'Please provide at most 100 items each time!'}, status=400)

			flag = False
			for i in range(len(body)):
				r = put_order(i, body[i], api_obj)
				flag = flag or r

			if flag:
				return JsonResponse({'Message': 'Your order(s) is(are) being processed!'})
			else:
				return JsonResponse({'Message': 'Invalid quantity in orders'}, status=400)

		return JsonResponse({'Message': 'Bad Request'}, status=400)

	return JsonResponse({'Message': 'Invalid API!'}, status=400)

def put_order(i, content, api_obj):
	sku = content['sku']
	try:
		qty = int(content['quantity'])
		print(qty)
		if qty < 0:
			print('qty < 0 in order')
			return False
	except Exception as e:
		print('qty error')
		return False

	in_stock = Status.objects.get(description='In Stock')
	item_in_stock = Item.objects.filter(sku=sku, sellerAPI=api_obj,
										status=in_stock)
	if len(item_in_stock) == 0 or item_in_stock[0].quantity < qty:
		print('Insufficient quantity in stock!')
		return False

	item_in_stock[0].quantity -= qty
	item_in_stock[0].save()

	status_obj = Status.objects.get(description='Preparing for Shipment')
	Item.objects.create(sku=sku, sellerAPI=api_obj,
						quantity=qty, status=status_obj,
						shipping_address=content['address'])
	# Push notification
	seller = Seller.objects.filter(sellerAPI=api_obj)
	if len(seller) == 0:
		print('Could not find the seller')
	else:
		endpoint = seller[0].endpoint
		data = {"Message": 'Item status changed',
				"sku": sku,
				"quantity": qty,
				"status": 'Preparing for Shipment'}
		notification(endpoint, data)
		print('Order placed successfully!')

	return True

def notification(url, data):
	headers = {'Content-type': 'json'}
	try:
		r = requests.post(url, data=json.dumps(data), headers=headers)
	except Exception as e:
		print('Invalid endpoint!')
		return -1
	else:
		return r.status_code
