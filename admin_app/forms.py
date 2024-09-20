from django import forms
from icons_app.models import Category,Category_Shape,Category_Type,Image,Gradient_Category,Sub_Gradient_Category,Gradient_Image,SubscriptionPlan,request_quote,Subscription,Image

# from .models import AdminUser

# class AdminRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = AdminUser
#         fields = ['username', 'email', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data

# class AdminLoginForm(forms.Form):
#     username = forms.CharField(max_length=150)
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if not AdminUser.objects.filter(username=username).exists():
#             raise forms.ValidationError("Invalid username")
#         return username

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'cat_image']


class CategoryTypeForm(forms.ModelForm):
    class Meta:
        model = Category_Type
        fields = ['category_type']


class CategoryShapeForm(forms.ModelForm):
    class Meta:
        model = Category_Shape
        fields = ['category_shape']


class ImagePlanForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_plan']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'image_name', 'category', 'image_plan', 'category_type', 'category_shape']


class GradientCategoryForm(forms.ModelForm):
    class Meta:
        model = Gradient_Category
        fields = ['gradient_category']


class SubGradientCategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Gradient_Category
        fields = ['sub_gradient_category', 'gradient_category']
        widgets = {
            'gradient_category': forms.Select(attrs={'class': 'form-control'}),
        }

class GradientImageForm(forms.ModelForm):
    class Meta:
        model = Gradient_Image
        fields = ['gradient_image', 'sub_gradient_category']





class RequestQuoteForm(forms.ModelForm):
    class Meta:
        model = request_quote
        fields = ['user', 'name', 'service', 'description', 'rq_image']


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'price']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['user', 'plan', 'payment_id', 'start_date', 'expiry_date', 'is_active']