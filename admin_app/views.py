from django.shortcuts import render, redirect, get_object_or_404
from icons_app.models import Category,Category_Shape,Category_Type,Image,Gradient_Category,Sub_Gradient_Category,Gradient_Image,Register,request_quote,Subscription
from .forms import CategoryForm, CategoryTypeForm, CategoryShapeForm,ImageForm,GradientCategoryForm,SubGradientCategoryForm,GradientImageForm,PaymentForm,RequestQuoteForm
from django.contrib.auth import authenticate, login

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Admin_Register

# Create your views here.

def admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if 'admin_id' not in request.session:
            return redirect('admin_app:admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def admin_register(request):
    if request.method == 'POST':
        a_username = request.POST.get('a_username')
        a_password = request.POST.get('a_password')

        hashed_password = make_password(a_password)
        new_user = Admin_Register(a_username=a_username, a_password=hashed_password)
        new_user.save()

        return redirect('admin_app:admin_login')

    return render(request, 'admin_reg.html')

def admin_login(request):
    if request.method == 'POST':
        a_username = request.POST['a_username']
        a_password = request.POST['a_password']

        try:
            user = Admin_Register.objects.get(a_username=a_username)
            if check_password(a_password, user.a_password):
                request.session['admin_id'] = user.id
                messages.success(request, 'Login successful!')
                return redirect('admin_app:admin_index')
            else:
                messages.error(request, 'password')
        except Admin_Register.DoesNotExist:
            messages.error(request, 'password')
    return render(request,'admin_login.html')


def admin_logout(request):
    del request.session['admin_id']
    return redirect('admin_app:admin_login')

@admin_required
def admin_index(request):
    user_count = Register.objects.count()
    message_count = request_quote.objects.count()
    total_images_count = Image.objects.count()
    context = {
        'user_count': user_count,
        'message_count':message_count,
        'total_images_count':total_images_count,
    }
    return render(request, 'admin_index.html', context)

@admin_required
def category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_app:category_view')  # Redirect to the same page to avoid resubmission
    else:
        form = CategoryForm()
    
    # Get the list of categories
    categories = Category.objects.all()

    return render(request, 'category_list.html', {'form': form, 'categories': categories})

@admin_required
def add_shape(request):
    if request.method == 'POST':
        shape_name = request.POST['category_shape']
        Category_Shape.objects.create(category_shape=shape_name)
        return redirect('admin_app:list_category_types')  # Ensure this matches a valid URL name
    return render(request, 'admin_app:list_category_types')

@admin_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_app:category_view')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'edit_category.html', {'form': form, 'category': category})

@admin_required
def edit_shape(request, id):
    shape = get_object_or_404(Category_Shape, pk=id)

    if request.method == 'POST':
        form = CategoryShapeForm(request.POST, instance=shape)
        if form.is_valid():
            form.save()
            return redirect('admin_app:list_category_types')  # Redirect to the list view after saving
    else:
        form = CategoryShapeForm(instance=shape)
    
    return render(request, 'edit_shape.html', {'form': form})

@admin_required
def confirm_delete_shape(request, id):
    shape = get_object_or_404(Category_Shape, pk=id)

    if request.method == 'POST':
        shape.delete()
        return redirect('admin_app:list_category_types')  # Redirect to the list view after deleting

    return render(request, 'confirm_delete_shape.html', {'shape': shape})

@admin_required
def confirm_delete_category(request, id):
    category = get_object_or_404(Category, pk=id)

    if request.method == 'POST':
        category.delete()
        return redirect('admin_app:category_view')  # Redirect to the list view after deletion

    return render(request, 'confirm_delete_category.html', {'category': category})

@admin_required
def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect('admin_app:category_view') 

@admin_required
def list_category_types(request):
    category_types = Category_Type.objects.all()
    shapes = Category_Shape.objects.all()
    return render(request, 'list_category_type.html', {'category_types': category_types,'shapes': shapes})

@admin_required
def add_category_type(request):
    if request.method == 'POST':
        category_type_name = request.POST.get('category_type')
        Category_Type.objects.create(category_type=category_type_name)
        return redirect('admin_app:list_category_types')
    return redirect('admin_app:list_category_types')

@admin_required
def edit_category_type(request, id):
    category_type = get_object_or_404(Category_Type, id=id)
    if request.method == 'POST':
        category_type.category_type = request.POST.get('category_type')
        category_type.save()
        return redirect('admin_app:list_category_types')
    return render(request, 'edit_category_type.html', {'category_type': category_type})

@admin_required
def delete_category_type(request, id):
    category_type = get_object_or_404(Category_Type, id=id)
    category_type.delete()
    return redirect('admin_app:list_category_types')

@admin_required
def add_icon(request):
    categories = Category.objects.all()
    types = Category_Type.objects.all()
    shapes = Category_Shape.objects.all()
    plans = Image.objects.all()
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_app:list_icons')
    else:
        form = ImageForm()

    context = {
        'form': form,
        'categories': categories,
        'types': types,
        'shapes': shapes,
        'plans': plans,
    }

    return render(request, 'add_icon.html', context)

@admin_required
def list_icons(request):
    icons = Image.objects.all()
    context = {
        'icons': icons,
    }
    return render(request, 'list_icons.html', context)

@admin_required
def edit_icon(request, icon_id):
    icon = get_object_or_404(Image, id=icon_id)
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=icon)
        if form.is_valid():
            form.save()
            return redirect('admin_app:list_icons')
    else:
        form = ImageForm(instance=icon)
    
    categories = Category.objects.all()
    types = Category_Type.objects.all()
    shapes = Category_Shape.objects.all()
    plans = Image.objects.all()

    context = {
        'form': form,
        'icon': icon,
        'categories': categories,
        'types': types,
        'shapes': shapes,
        'plans': plans,
    }

    return render(request, 'edit_icon.html', context)

@admin_required
def delete_icon(request, icon_id):
    icon = get_object_or_404(Image, id=icon_id)
    icon.delete()
    return redirect('admin_app:list_icons')


@admin_required
def gradient_category_list(request):
    gradients = Gradient_Category.objects.all()
    sub_gradients = Sub_Gradient_Category.objects.all()

    if request.method == 'POST':
        if 'add_gradient' in request.POST:
            gradient_form = GradientCategoryForm(request.POST)
            if gradient_form.is_valid():
                gradient_form.save()
                return redirect('admin_app:gradient_category_list')
        elif 'add_sub_gradient' in request.POST:
            sub_gradient_form = SubGradientCategoryForm(request.POST)
            if sub_gradient_form.is_valid():
                sub_gradient_form.save()
                return redirect('admin_app:gradient_category_list')
    else:
        gradient_form = GradientCategoryForm()
        sub_gradient_form = SubGradientCategoryForm()

    return render(request, 'gradient_category_list.html', {
        'gradients': gradients,
        'sub_gradients': sub_gradients,
        'gradient_form': gradient_form,
        'sub_gradient_form': sub_gradient_form,
    })

@admin_required
def edit_gradient_category(request, id):
    gradient = get_object_or_404(Gradient_Category, id=id)
    if request.method == 'POST':
        form = GradientCategoryForm(request.POST, instance=gradient)
        if form.is_valid():
            form.save()
            return redirect('admin_app:gradient_category_list')
    else:
        form = GradientCategoryForm(instance=gradient)
    return render(request, 'edit_gradient_category.html', {'form': form})

@admin_required
def confirm_delete_gradient(request, id):
    gradient = get_object_or_404(Gradient_Category, id=id)
    if request.method == 'POST':
        gradient.delete()
        return redirect('admin_app:gradient_category_list')
    return render(request, 'confirm_delete_gradient.html', {'object': gradient})

@admin_required
def delete_gradient_category(request, id):
    gradient = get_object_or_404(Gradient_Category, id=id)
    if request.method == 'POST':
        gradient.delete()
        return redirect('admin_app:gradient_category_list')
    return redirect('admin_app:gradient_category_list')  # Redirect if method is not POST

@admin_required
def edit_sub_gradient_category(request, id):
    sub_gradient = get_object_or_404(Sub_Gradient_Category, id=id)
    if request.method == 'POST':
        form = SubGradientCategoryForm(request.POST, instance=sub_gradient)
        if form.is_valid():
            form.save()
            return redirect('admin_app:gradient_category_list')
    else:
        form = SubGradientCategoryForm(instance=sub_gradient)
    return render(request, 'edit_sub_gradient_category.html', {'form': form})

@admin_required
def delete_sub_gradient_category(request, id):
    sub_gradient = get_object_or_404(Sub_Gradient_Category, id=id)
    if request.method == 'POST':
        sub_gradient.delete()
        return redirect('admin_app:gradient_category_list')
    return render(request, 'confirm_delete_sub_gradient.html', {'object': sub_gradient})

@admin_required
def confirm_delete_sub_gradient(request, id):
    sub_gradient = get_object_or_404(Sub_Gradient_Category, id=id)
    if request.method == 'POST':
        sub_gradient.delete()
        return redirect('admin_app:gradient_category_list')
    return render(request, 'confirm_delete_sub_gradient.html', {'object': sub_gradient})

@admin_required
def gradient_image_list(request):
    if request.method == 'POST':
        form = GradientImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_app:gradient_image_list')  # Redirect to the same page to avoid form resubmission
    else:
        form = GradientImageForm()

    gradient_images = Gradient_Image.objects.all()
    return render(request, 'gradient_image_list.html', {
        'form': form,
        'gradient_images': gradient_images
    })

@admin_required
def edit_gradient_image(request, id):
    gradient_image = get_object_or_404(Gradient_Image, id=id)
    
    if request.method == 'POST':
        form = GradientImageForm(request.POST, request.FILES, instance=gradient_image)
        if form.is_valid():
            form.save()
            return redirect('admin_app:gradient_image_list')
    else:
        form = GradientImageForm(instance=gradient_image)
    
    return render(request, 'edit_gradient_image.html', {'form': form})

@admin_required
def delete_gradient_image(request, id):
    gradient_image = get_object_or_404(Gradient_Image, id=id)
    
    if request.method == 'POST':
        gradient_image.delete()
        return redirect('admin_app:gradient_image_list')
    
    return render(request, 'confirm_delete_gradient_image.html', {'object': gradient_image})

@admin_required
def list_payments(request):
    payments = Subscription.objects.all()
    return render(request, 'payment_list_admin.html', {'payments': payments})

@admin_required
def chatbox(request):
    quotes = request_quote.objects.all()
    return render(request, 'chatbox.html', {'r_quote': quotes})

@admin_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(request_quote, id=chat_id)
    return render(request, 'chatbox.html', {'chat': chat})

@admin_required
def chatbox_view(request, chat_id):
    chat = get_object_or_404(request_quote, id=chat_id)
    other_users = Register.objects.exclude(id=chat.user.id)
    r_quote = request_quote.objects.all()

    context = {
        'chat': chat,
        'other_users': other_users,
        'r_quote': r_quote
    }
    return render(request, 'chatbox.html', context)

@admin_required
def user_detail_view(request, user_id):
    user = get_object_or_404(Register, id=user_id)
    context = {
        'user': user
    }
    return render(request, 'user_detail.html', context)

@admin_required
def send_reply_view(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        reply = request.POST.get('reply')
        chat = get_object_or_404(request_quote, id=chat_id)

    return redirect('admin_app:chatbox', chat_id=chat_id)

@admin_required
def send_reply(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        reply = request.POST.get('reply')
        chat = get_object_or_404(request_quote, id=chat_id)
      
        send_mail(
            subject=f"Reply to your request: {chat.name}",
            message=reply,
            from_email='iconsdott@gmail.com', 
            recipient_list=[chat.user.email]
        )
        return HttpResponseRedirect(reverse('admin_app:chatbox'))  

    return HttpResponseRedirect(reverse('admin_app:chatbox'))