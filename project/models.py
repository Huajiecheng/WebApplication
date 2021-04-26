from django.db import models
from django import forms

from django.contrib.auth.models import User

# Create your models here.

class Entry(models.Model):
    TYPE_CHOICES = (
        ("Appetizer", "Appetizer"),
        ("Soup", "Soup"),
        ("Salad","Salad"),
        ("Entree", "Entree"),
        ("Beverage", "Beverage"),
        ("Dessert", "Dessert"),
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    entry_type = models.CharField(max_length=30, choices = TYPE_CHOICES, default = "")
    name = models.CharField(max_length=30)
    def __str__(self):
        return 'Entry(id=' + str(self.id) + ')'



state_abbr = {'Alabama':'AL','Alaska':'AK','Arizona': 'AZ','Arkansas':'AR','California':'CA','Colorado':'CO',
              'Connecticut':'CT','District of Columbia':'DC','Delaware':'DE','Florida':'FL','Georgia':'GA',
              'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY',
              'Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN',
              'Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH',
              'New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND',
              'Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC',
              'South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA',
              'Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

states_choices = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", 
                  "Colorado", "Connecticut", "Delaware", "District Of Columbia", 
                  "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", 
                  "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
                  "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
                  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
                  "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
                  "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
                  "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                  "West Virginia", "Wisconsin", "Wyoming"]


class AddressProfile(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    picture = models.FileField(blank=True, default = None)
    content_type = models.CharField(max_length=50, default = "")
    postal_code = models.CharField(max_length=5, default="")
    state = models.CharField(max_length = 100, default = "")
    street_1 = models.CharField(max_length = 200, default = "")
    street_2 = models.CharField(max_length = 200, default = "")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.state:
            self.state= eval(self.state)

    def __str__(self):
        return 'Address Profile(id=' + str(self.id) + ')'



class Cart(models.Model):
    owner = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    def __str__(self):
        return 'Cart(id=' + str(self.id) + ')'

class CartEntry(models.Model):
    entry = models.ForeignKey(Entry, default=None, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return 'CartEntry(id=' + str(self.id) + ')'
    def subtotal(self):
        return self.quantity * self.entry.price

class Order(models.Model):
    TYPE_CHOICES = (
        ("COMPLETE", "Complete"),
        ("INPROGRESS", "In Progress"),
        ("CANCELLED","Cancelled"),
    )
    status = models.CharField(max_length=30, choices = TYPE_CHOICES, default = "")
    customer = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    instruction = models.CharField(max_length=200,default = "")
    order_time = models.DateTimeField()
    location = models.CharField(max_length=200, default = "")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return 'Order(id=' + str(self.id) + ')'

class OrderEntry(models.Model):
    entry = models.ForeignKey(Entry, default=None, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return 'OrderEntry(id=' + str(self.id) + ')'    
    def subtotal(self):
        return self.quantity * self.entry.price 


class ReviewImage(models.Model):
    image = models.FileField(upload_to='reviewImages/',blank=True, default = None)
    content_type = models.CharField(max_length=50, default = "")

class Review(models.Model):
    order = models.ForeignKey(Order,default=None,on_delete=models.PROTECT)
    review_text = models.CharField(max_length=200)
    rating = models.FloatField()
    images = models.ManyToManyField(ReviewImage)
    profile = models.ForeignKey(AddressProfile, default=None, on_delete=models.PROTECT)
    review_time = models.DateTimeField()
    def __str__(self):
        return 'Review(id=' + str(self.id) + ')'




class Restaurant(models.Model):
    admin_user = models.ForeignKey(User, default=None,on_delete=models.PROTECT)
    name = models.CharField(max_length=200, default="your restaurant's name")
    photo = models.FileField(blank=True, default = None)
    content_type = models.CharField(max_length=50, default = "")
    description = models.CharField(max_length=200, default="your restaurant's description")
    location = models.CharField(max_length=200, default="your restaurant's location")
    average_rating = models.FloatField(default=0)
    num_review = models.IntegerField(default=0)
    deliveryTime = models.CharField(max_length=200, default="Estimated time?")

    