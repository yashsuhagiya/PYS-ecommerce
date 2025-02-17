from django.contrib.postgres.fields import ArrayField
from django.db import models

class Address(models.Model):
	first_len = models.CharField(max_length=200,null=False)
	second_len = models.CharField(max_length=200,null=False)
	city = models.CharField(max_length=200,null=False)
	state = models.CharField(max_length=30,null=False)
	pincode = models.IntegerField( null=False)
	primary_address = models.BooleanField(default=False)

	def __str__(self): 
         return self.first_len+" "+self.second_len

class Customer(models.Model):
	firstname = models.CharField(max_length=200,null=False)
	lastname = models.CharField(max_length=200,null=False)
	email = models.CharField(max_length=200,null=False)
	password = models.CharField(max_length=200,null=False)
	mobile_no = models.BigIntegerField(null=False,blank=False)
	gender = models.CharField(max_length=20,default="Male")
	search = ArrayField(
    	base_field=models.CharField(max_length=10),
    	size=5,
    	max_length=(5*11),
    	null=True,
    	default=list  # or default=list() depending on Django version
	)

	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return str(self.id)

class Product(models.Model):
	RATE = (
        ('1', 'Very Low'),
        ('2', 'Low'),
        ('3', 'Avarage'),
		('4', 'Good'),
		('5', 'Very Good'),
    )

	# product_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
	image = models.ImageField(null=True, blank=True)
	category = ArrayField(
		base_field = models.CharField(max_length=10),
		size = 5,
		max_length = (5*11),
	)
	stock = models.IntegerField(default=0)
	color = models.CharField(max_length=20,null=True)
	size = ArrayField(
		base_field = models.CharField(max_length=3),
		size = 6,
		max_length = (6*4),
	)
	description = models.CharField(max_length=200,null=True)
	rating = models.IntegerField(choices=RATE,default=5)
	discount = models.IntegerField(default=0)

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
        # Convert the comma-separated string to a list
		if isinstance(self.category, str):
			self.category = self.category.split(',')
		if isinstance(self.size, str):
			self.size = self.size.split(',')

		super().save(*args, **kwargs)

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	STATUS = (
		('Pending','Pending'),
		('Out for delivery','Out for delivery'),
		('Delivered','Delivered'),
	)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)
	date_ordered = models.DateTimeField()
	status = models.CharField(max_length=40, null=True, choices=STATUS)
	transaction_id = models.CharField(max_length=200,null=True,blank=True,default="00000000")
	method = models.CharField(max_length=40, null=False, default="COD")

	def __str__(self):
		return self.transaction_id

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField( default=1)
	date_added = models.DateTimeField()
	delivered = models.CharField(max_length=50,default="Ordered")
	rating = models.IntegerField(default=0)

	def __str__(self):
		return str(self.product.name+" "+self.order.customer.firstname)

class Paymentdata(models.Model):
	orderid = models.CharField(max_length=200)
	cid = models.CharField(max_length=50)
	

class shopping_cart(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=True)
	quantity = models.IntegerField( null=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=True)

class Admin_detail(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=15)
