from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 


def _get_session_cart(request):
	cart = request.session.get("cart")
	if cart is None:
		cart = {}
		request.session["cart"] = cart
	return cart


def Home(request):
	menu_list = Menu.objects.all().order_by('-id')[:3]
	return render(request, "index.html", locals())

@login_required
def finishOrder(request,pk):
	employee = Employee.objects.get(user=request.user)
	order = Order.objects.get(id=pk)
	order.mark_ready(employee)
	return redirect("order")

@login_required
def receiveOrder(request,pk):
	order = Order.objects.get(id=pk)
	if order.available and not order.delivered:
		order.mark_delivered()
	return redirect("order")

@login_required
def Create_order(request,pk):
	client = Client.objects.get(user=request.user)
	menu = Menu.objects.get(id=pk)
	order = Order(
		client = client,
		menu =menu
		)
	order.save()
	return redirect("order")

def Menuview(request):
	menu_list = Menu.objects.all()
	return render(request, "menu.html",locals())


@login_required
def add_to_cart(request, id):
	menu_item = Menu.objects.get(id=id)
	cart = _get_session_cart(request)
	item_id = str(menu_item.id)
	if item_id in cart:
		cart[item_id]["quantity"] += 1
	else:
		cart[item_id] = {
			"name": menu_item.name,
			"price": int(menu_item.price),
			"quantity": 1,
		}
	request.session["cart"] = cart
	request.session.modified = True
	messages.success(request, "Item added to cart")
	return redirect("cart")


@login_required
def remove_from_cart(request, id):
	cart = _get_session_cart(request)
	item_id = str(id)
	if item_id in cart:
		del cart[item_id]
		request.session["cart"] = cart
		request.session.modified = True
		messages.success(request, "Item removed from cart")
	return redirect("cart")


@login_required
def increase_quantity(request, id):
	cart = _get_session_cart(request)
	item_id = str(id)
	if item_id in cart:
		cart[item_id]["quantity"] += 1
		request.session["cart"] = cart
		request.session.modified = True
		messages.success(request, "Quantity increased")
	return redirect("cart")


@login_required
def decrease_quantity(request, id):
	cart = _get_session_cart(request)
	item_id = str(id)
	if item_id in cart:
		if cart[item_id]["quantity"] > 1:
			cart[item_id]["quantity"] -= 1
			messages.success(request, "Quantity decreased")
		else:
			del cart[item_id]
			messages.success(request, "Item removed from cart")
		request.session["cart"] = cart
		request.session.modified = True
	return redirect("cart")


@login_required
def cart_view(request):
	cart = _get_session_cart(request)
	cart_items = []
	grand_total = 0
	for item_id, item in cart.items():
		total = item["price"] * item["quantity"]
		grand_total += total
		cart_items.append(
			{
				"id": item_id,
				"name": item["name"],
				"price": item["price"],
				"quantity": item["quantity"],
				"total": total,
			}
		)
	return render(request, "cart.html", {"cart_items": cart_items, "grand_total": grand_total})

def register_profil(request):
	user_form = RegistrationUserForm(request.POST or None)
	client_form = ClientForm(request.POST or None)
	if (request.method=='POST'):
		if user_form.is_valid() and client_form.is_valid():
			user = user_form.save()
			client_group = Group.objects.get(name="Client")
			user.groups.add(client_group)
			client = client_form.save(commit=False)
			client.user = user
			client.save()
			if user:
				login(request, user)
				return redirect("home")
			return redirect("connect")
	return render(request, 'register.html',locals())

def connexion(request):
	connexion_form=ConnexionForm(request.POST)
	if (request.method == 'POST'):
		if connexion_form.is_valid():
			username=connexion_form.cleaned_data['username']
			password=connexion_form.cleaned_data['password']
			user=authenticate(username=username,password=password)#verification donnée
			if user:#si l'objet existe 
				login(request, user)
				return redirect("home") #on connecte l'utilisateur
			else:
				connexion_form=ConnexionForm()
	else:
		connexion_form=ConnexionForm()	
	return render(request, 'login.html', locals())

def deconnexion(request):
	logout(request)
	return redirect("home")

@login_required
def orderview(request):
	group = request.user.groups.first()
	orderList = []
	if not group:
		return render(request, "order.html", locals())
	group_name = str(group)
	if group_name == "Client":
		client = Client.objects.get(user=request.user)
		orderList = Order.objects.filter(client = client)
	
	elif group_name == "Chef":
		orderList = Order.objects.filter(delivered=False)
	return render(request, "order.html",locals())


def aboutview(request):
	return render(request, "about.html",locals())
