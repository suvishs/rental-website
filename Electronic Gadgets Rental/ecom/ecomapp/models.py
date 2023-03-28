from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=35)
    maritial_status = models.CharField(max_length=35)
    occupation = models.CharField(max_length=100)
    email = models.EmailField()
    anual_income = models.IntegerField()
    aadhar_number = models.IntegerField()
    pan_number = models.IntegerField()
    pancard_image_front = models.ImageField(upload_to="pan_front_img")
    pancard_image_back = models.ImageField(upload_to="pan_back_img")
    bankstatement = models.FileField(upload_to="bankstatement")

    net_pay = models.IntegerField(null=True)
    lender_score = models.FloatField(null=True)

    permanant_adress = models.CharField(max_length=255)
    approval = models.BooleanField(default=False)
    usr = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=255)
    price = models.CharField(max_length=10, null=True)
    rental_price = models.CharField(max_length=10)
    product_image = models.ImageField(upload_to="product_img")



class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class RentedItems(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    quantity = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    total_amount_dis = models.FloatField(null=True)


 



