from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="employee_user")
	birthday =models.DateField(default=timezone.now)
	gender =models.CharField(max_length=100)
	phone =models.CharField(max_length=100)

	def __str__(self):
		return self.user.username

class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="client_user")
	birthday =models.DateField(default=timezone.now)
	gender =models.CharField(max_length=100, null = True)
	phone =models.CharField(max_length=100, null = True)
	address=models.CharField(max_length=100, null = True)

	def __str__(self):
		return f"{self.user.username} - Client"
	
class Menu(models.Model):
	name=models.CharField(max_length=100)
	description=models.TextField()
	photos=models.ImageField(upload_to='Images/Menus/')
	price=models.PositiveIntegerField()

	def __str__(self):
		return f'Name:{self.name}--Price:{self.price}'

class Drink(models.Model):
	name=models.CharField(max_length=100)
	price=models.PositiveIntegerField()

	def __str__(self):
		return self.name

class Order(models.Model):
	client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
	menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
	drink=models.ForeignKey(Drink,on_delete=models.CASCADE,null=True)
	available=models.BooleanField(default = False)
	delivered=models.BooleanField(default = False)
	employee=models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
	datetime=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Order {self.id} - {self.menu.name}"

	def mark_ready(self, employee):
		self.available = True
		self.employee = employee
		self.save()

	def mark_delivered(self):
		self.delivered = True
		self.save()
