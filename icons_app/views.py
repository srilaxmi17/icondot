from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import *
import uuid,razorpay
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Register.objects.filter(email=email).exists():
            error_message = "Email already taken"
            return render(request, 'registration.html', {'error': error_message})

        hashed_password = make_password(password)
        new_user = Register(username=username, email=email, password=hashed_password)
        new_user.save()

        return redirect('icons_app:login')

    return render(request, 'registration.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Register.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['umail'] = email
                messages.success(request, 'Login successful!')
                return redirect('icons_app:index')
            else:
                messages.error(request, 'Invalid email or password')
        except Register.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request,'login.html')

# def index(request, cat_id=None, type_id=None, shape_id=None):
#     user_id = request.session.get('user_id')
#     user_email = request.session.get('user_email')
#     category = Category.objects.all()
#     category_type = Category_Type.objects.all()
#     category_shape = Category_Shape.objects.all()
    
#     # Start with all images
#     image_cat = Image.objects.all()
    
#     # Apply filters if they exist
#     if cat_id:
#         image_cat = image_cat.filter(category=cat_id)
#     if type_id:
#         image_cat = image_cat.filter(category_type=type_id)
#     if shape_id:
#         image_cat = image_cat.filter(category_shape=shape_id)
    
#     context = {
#         'image_cat': image_cat,
#         'category': category,
#         'category_type': category_type,
#         'category_shape': category_shape,
#         'user_email': user_email
#     }
#     return render(request, 'index.html', context)





def index(request):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    category = Category.objects.all()
    category_type = Category_Type.objects.all()
    category_shape = Category_Shape.objects.all()


    is_subscribed = False
    if user_id:
        register_user = Register.objects.filter(id=user_id).first()
        if register_user:
            active_subscription = Subscription.objects.filter(user=register_user, is_active=True).exists()
            if active_subscription:
                is_subscribed = True

    # Get filter parameters from request
    cat_id = request.GET.get('cat_id')
    type_id = request.GET.get('type_id')
    shape_id = request.GET.get('shape_id')

    # Start with all images
    filtered_images = Image.objects.all()

    # Apply filters if they exist
    if cat_id:
        filtered_images = filtered_images.filter(category_id=cat_id)
    if type_id:
        filtered_images = filtered_images.filter(category_type_id=type_id)
    if shape_id:
        filtered_images = filtered_images.filter(category_shape_id=shape_id)

    context = {
        'image_cat': filtered_images,
        'category': category,
        'category_type': category_type,
        'category_shape': category_shape,
        'user_email': user_email,
        'is_subscribed': is_subscribed,
    }
    print(user_id)
    return render(request, 'index.html', context)




def logout(request):
    del request.session['user_id']
    del request.session['umail']
    return redirect('icons_app:index')

def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                user = Register.objects.get(email=email)
                user.reset_token = uuid.uuid4()
                user.reset_token_expires = timezone.now() + timezone.timedelta(hours=1)
                user.save()

                # Generate reset link
                reset_link = request.build_absolute_uri(f'/reset-password/{user.reset_token}/')

                # Send the email
                send_mail(
                    'Password Reset Request',
                    f'Click the link below to reset your password:\n{reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, 'Password reset link sent to your email!')
            except Register.DoesNotExist:
                messages.error(request, 'Entered mail address is not registed.')
                return redirect('icons_app:request_password_reset')  # Redirect to registration page if user not found
        else:
            messages.error(request, 'Invalid email address.')
    return render(request, 'password_reset_request.html')


def reset_password(request, token):
    try:
        user = Register.objects.get(reset_token=token, reset_token_expires__gte=timezone.now())
    except Register.DoesNotExist:
        messages.error(request, 'Invalid or expired reset token.')
        return redirect('icons_app:login')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user.set_password(new_password)
            user.reset_token = None
            user.reset_token_expires = None
            user.save()
            messages.success(request, 'Password reset successful!')
            return redirect('icons_app:login')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'password_reset.html')

def export_icons(request):
    return render(request,'registration.html')



def subscription(request,gradientcategory_id=None):
    gradient_category = Gradient_Category.objects.all()
    if gradientcategory_id:
        # selected_category = get_object_or_404(Gradient_Category, id=gradientcategory_id)
        sub_gradient_category = Sub_Gradient_Category.objects.filter(gradient_category=gradientcategory_id)
    else:
        sub_gradient_category = Sub_Gradient_Category.objects.all()
    user_id = request.session.get('user_id')
    umail = request.session.get('umail')

    # user = get_object_or_404(Register, pk=user_id)
    active_subscription = Subscription.objects.filter(user=user_id, is_active=True).exists()
    active_c_subscription = Subscription.objects.filter(user=user_id, is_active=True).first()
    # reminder_popup = False
    # if active_c_subscription and active_c_subscription.expiry_date <= timezone.now() + timedelta(days=2):
    #     reminder_popup = True

    # reminder_popup = False
    # if active_c_subscription:
    #     expiry_date = active_c_subscription.expiry_date.date()
    #     current_date = datetime.now().date()  # Get the current date as a date object
    #     days_to_expiry = (expiry_date - current_date).days
    #     if days_to_expiry <= 3:  # Trigger the reminder if the plan is expiring within 7 days
    #         reminder_popup = True

    # print(f"User: {user.username}, Active Subscription: {active_subscription}")


    context = {
        'active_subscription': active_subscription,
        'active_c_subscription': active_c_subscription,
        'gradient_category': gradient_category,
        'sub_gradient_category': sub_gradient_category,
        # 'reminder_popup':reminder_popup,
        # 'days_to_expiry':days_to_expiry,
    }


    if request.method == 'POST':
        if umail:
            email = request.POST.get('email') 
            name = request.POST.get('name')
            gradient_category_id = request.POST.get('gradientcategory')
            description = request.POST.get('description')
            rq_image = request.FILES.get('rq_image')
            mail=Register.objects.get(email=email)
            gradient_category=Gradient_Category.objects.get(id=gradient_category_id)
            try:
                gradient_category_obj = Gradient_Category.objects.get(id=gradient_category_id)
            except Exception as e:
                print(e)

            request_quote.objects.create(user=mail,name=name,service=gradient_category,description=description,rq_image=rq_image)    
            print(email, name, gradient_category, description, rq_image)
    return render(request, 'page2.html', context)

def sub_gra(request,id):
    gradient_image=Gradient_Image.objects.filter(sub_gradient_category=id)
    return render(request,'page2.html')

# def gra_img(request,id):
#     gradient_image=Gradient_Image.objects.filter(sub_gradient_category=id)
#     sub_gradient_category = Sub_Gradient_Category.objects.all()
#     context={'gradient_image':gradient_image,'sub_gradient_category':sub_gradient_category}
#     return render(request,'gra_img.html',context)

def gra_img(request, id):
    gradient_image = Gradient_Image.objects.filter(sub_gradient_category=id)
    sub_gradient_category = Sub_Gradient_Category.objects.all()

    subgradient_category = get_object_or_404(Sub_Gradient_Category, id=id)
    total_likes = PageLike.objects.filter(sub_gradient_category=subgradient_category).count()
    
    user_has_liked = False
    user_id = request.session.get('user_id')

    if user_id:
        # Only check if the user is logged in
        register_user = Register.objects.filter(id=user_id).first()
        if register_user:
            user_has_liked = PageLike.objects.filter(user=register_user, sub_gradient_category=subgradient_category).exists()


    context = {
        'gradient_image': gradient_image,
        'sub_gradient_category': sub_gradient_category,
        'subgradient_category': subgradient_category,
        'total_likes': total_likes,
        'user_has_liked': user_has_liked,
    }
    return render(request, 'gra_img.html', context)


def like_page(request, id):
    sub_gradient_category = get_object_or_404(Sub_Gradient_Category, id=id)
    user_id = request.session.get('user_id')

    # Fetch the Register instance using the user_id from the session
    register_user = get_object_or_404(Register, id=user_id)

    # Check if the user has already liked this page
    page_like = PageLike.objects.filter(user=register_user, sub_gradient_category=sub_gradient_category).first()

    if page_like:
        # Unlike (remove the like)
        page_like.delete()
    else:
        # Like (add a new like)
        PageLike.objects.create(user=register_user, sub_gradient_category=sub_gradient_category)

    return redirect('icons_app:gra_img', id=id)


def test(request):
    requestquote=request_quote.objects.all()
    context={'requestquote':requestquote}
    return render(request,'text.html',context)   

def terms(request):
    return render(request,'terms.html')

def privacy(request):
    return render(request,'privacy.html')

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def subscribeplan(request, plan_name):
    # Fetch the selected plan
    plan = get_object_or_404(SubscriptionPlan, name=plan_name)
    amount = int(plan.price * 100*12)  # Convert to paisa (for INR)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"  # Auto-capture the payment
    })

    context = {
        'plan': plan,
        'amount': amount,
        'order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,  # Fetching Razorpay Key ID from settings
    }

    return render(request, 'payment.html', context)

def payment_confirmation(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        print("User ID not found in session.")
        return redirect('login_page')  # Redirect to login if the user is not authenticated

    if request.method == 'POST':
        plan_name = request.POST.get('plan_name')
        payment_id = request.POST.get('razorpay_payment_id')

        print(f"Received POST data - Plan Name: {plan_name}, Payment ID: {payment_id}, User ID: {user_id}")

        if not payment_id:
            print("Payment ID not received.")
            return redirect('icons_app:subscription')  # Handle error

        try:
            plan = get_object_or_404(SubscriptionPlan, name=plan_name)
            user = get_object_or_404(Register, pk=user_id)

            print(f"Plan found: {plan}, User found: {user}")

            subscription = Subscription.objects.create(
                user=user,
                plan=plan,
                payment_id=payment_id,
                start_date=timezone.now(),
                expiry_date=timezone.now() + timedelta(days=365),
            )

            print(f"Subscription created: {subscription}")
            return redirect('icons_app:success_page')
        except Exception as e:
            print(f"Error creating subscription: {e}")
            return redirect('icons_app:subscription')  # Handle error

    print("Request method is not POST or payment failed.")
    return redirect('payment_confirmation')


def cancel_subscription(request):
    user_id = request.session.get('user_id')  # Retrieve the user_id from the session

    if not user_id:
        return redirect('login_page')  # Redirect to login if the user is not authenticated

    user = get_object_or_404(Register, pk=user_id)  # Fetch the corresponding Register instance

    # Now use the correct Register instance to query the Subscription model
    subscription = get_object_or_404(Subscription, user=user, is_active=True)
    subscription.is_active = False
    subscription.save()

    return redirect('icons_app:subscription')


def success_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_page')

    user = get_object_or_404(Register, pk=user_id)
    subscription = Subscription.objects.filter(user=user).order_by('-start_date').first()
    total_amount = subscription.plan.price * 12
    
    context = {
        'username': user.username,
        'plan_name': subscription.plan.name,
        'amount': total_amount,
    }
    return render(request, 'pay_success.html', context)


