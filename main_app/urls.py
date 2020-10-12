from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sneakers/', views.sneakers_index, name='index'),
    path('sneakers/<int:sneakers_id>/', views.sneakers_detail, name='detail'),
    path('sneakers/create/', views.SneakersCreate.as_view(), name='sneakers_create'),
    path('sneakers/<int:pk>/update/', views.SneakersUpdate.as_view(), name='sneakers_update'),
    path('sneakers/<int:pk>/delete/', views.SneakersDelete.as_view(), name='sneakers_delete'),
    path('sneakers/<int:sneakers_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),

]