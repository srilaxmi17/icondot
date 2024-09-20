from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views
app_name = 'admin_app'

urlpatterns = [

    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_register/',views.admin_register, name='admin_register'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('categories/',views. category_view, name='category_view'),
    path('add-shape/', views.add_shape, name='add_shape'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('shapes/<int:id>/edit/', views.edit_shape, name='edit_shape'),
    path('shapes/<int:id>/confirm-delete/', views.confirm_delete_shape, name='confirm_delete_shape'),
    path('categories/<int:id>/confirm-delete/', views.confirm_delete_category, name='confirm_delete_category'),
    path('categories/<int:id>/delete/', views.delete_category, name='delete_category'),
    path('category-types/', views.list_category_types, name='list_category_types'),
    path('add-category-type/', views.add_category_type, name='add_category_type'),
    path('edit-category-type/<int:id>/', views.edit_category_type, name='edit_category_type'),
    path('delete-category-type/<int:id>/', views.delete_category_type, name='delete_category_type'),
    path('add_icon/', views.add_icon, name='add_icon'),
    path('list_icons/', views.list_icons, name='list_icons'),
    path('icons/edit/<int:icon_id>/', views.edit_icon, name='edit_icon'),
    path('icons/delete/<int:icon_id>/', views.delete_icon, name='delete_icon'),
    path('gradient-category-list/', views.gradient_category_list, name='gradient_category_list'),
    path('edit-gradient-category/<int:id>/', views.edit_gradient_category, name='edit_gradient_category'),
   path('confirm-delete-gradient/<int:id>/',views. confirm_delete_gradient, name='confirm_delete_gradient'),
    path('delete-gradient-category/<int:id>/',views. delete_gradient_category, name='delete_gradient_category'),
    path('edit-sub-gradient-category/<int:id>/', views.edit_sub_gradient_category, name='edit_sub_gradient_category'),
    path('delete-sub-gradient-category/<int:id>/', views.delete_sub_gradient_category, name='delete_sub_gradient_category'),
    path('gradient-images/',views. gradient_image_list, name='gradient_image_list'),
    path('edit-gradient-image/<int:id>/',views. edit_gradient_image, name='edit_gradient_image'),
    path('delete-gradient-image/<int:id>/',views. delete_gradient_image, name='delete_gradient_image'),
    path('payments/', views.list_payments, name='list_payments'),

    path('chatbox/', views.chatbox, name='chatbox'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('send-reply/', views.send_reply, name='send_reply'),
   
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
