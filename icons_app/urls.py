from django.urls import path
from . import views

app_name = 'icons_app'


urlpatterns = [
    path('',views.index, name='index'),

    path('<int:cat_id>/', views.index, name='index'),
    path('<int:cat_id>/<int:type_id>/', views.index, name='index'),
    path('<int:cat_id>/<int:shape_id>/', views.index, name='index'),  # Category + Shape
    path('<int:cat_id>/<int:type_id>/<int:shape_id>/', views.index, name='index'),
    # path('<int:cat_id>',views.index, name='index'),
    # path('<int:type_id>/',views.index, name='index'),
    # path('<int:shape_id>',views.index, name='index'),

   

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('request_password_reset/', views.request_password_reset, name='request_password_reset'),
    path('reset-password/<uuid:token>/', views.reset_password, name='reset_password'),
    path('export_icons/', views.export_icons, name='export_icons'),
    path('subscription/', views.subscription, name='subscription'),
    path('subscription/<int:gradientcategory_id>/', views.subscription, name='subscription'),
    path('gra_img/<int:id>', views.gra_img, name='gra_img'),
    path('like-page/<int:id>/', views.like_page, name='like_page'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('subscription/<str:plan_name>/', views.subscribeplan, name='subscribeplan'),
    # path('payment-process/',views.payment_process, name='payment_process'),
    path('payment_confirmation',views.payment_confirmation, name='payment_confirmation'),
    path('cancel_subscription',views.cancel_subscription, name='cancel_subscription'),
    path('success_page',views.success_page, name='success_page'),
    
]