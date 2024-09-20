from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    reset_token = models.UUIDField(null=True, blank=True, unique=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
class Category(models.Model):
    category=models.CharField(max_length=35)
    cat_image=models.FileField(upload_to='cat_images/')

    def __str__(self):
        return self.category

class Category_Type(models.Model):
    category_type=models.CharField(max_length=35)

    def __str__(self):
        return self.category_type

class Category_Shape(models.Model):
    category_shape=models.CharField(max_length=35)

    def __str__(self):
        return self.category_shape
    

class Image(models.Model):
    IMAGE_PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Pro', 'Pro'),
    ]
    image=models.FileField(upload_to='images/')
    image_name=models.CharField(max_length=25) 
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image_plan=models.CharField(max_length=25,choices=IMAGE_PLAN_CHOICES)
    category_type=models.ForeignKey(Category_Type,on_delete=models.CASCADE)
    category_shape=models.ForeignKey(Category_Shape,on_delete=models.CASCADE)

    def __str__(self):
        return self.category.category

    
class Gradient_Category(models.Model):
    gradient_category=models.CharField(max_length=30)

    def __str__(self):
        return self.gradient_category

class Sub_Gradient_Category(models.Model):
    sub_gradient_category=models.CharField(max_length=30)  
    featured_image = models.ImageField(upload_to='sub_gradient_images/', null=True, blank=True)  # Added ImageField
    gradient_category=models.ForeignKey(Gradient_Category,on_delete=models.CASCADE,null=True,blank=True) 

    def __str__(self):
        return self.sub_gradient_category    

class Gradient_Image(models.Model):
    gradient_image=models.ImageField(upload_to='gradient_images/')
    sub_gradient_category=models.ForeignKey(Sub_Gradient_Category,on_delete=models.CASCADE) 

    def __str__(self):
        # Access the gradient_category through the sub_gradient_category
        gradient_category = self.sub_gradient_category.gradient_category
        return f'{gradient_category} - {self.gradient_image}'

class request_quote(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    name=models.CharField(max_length=35)
    service=models.CharField(max_length=35,null=True,blank=True)
    description=models.TextField(max_length=200)
    rq_image=models.ImageField(upload_to='re_images/')
    

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('personal', 'Personal'),
        ('team', 'Team'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return self.name    
    
class Subscription(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey('SubscriptionPlan', on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=365))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def cancel_subscription(self):
        self.is_active = False
        self.save()

class PageLike(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    sub_gradient_category = models.ForeignKey(Sub_Gradient_Category, on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'sub_gradient_category')        