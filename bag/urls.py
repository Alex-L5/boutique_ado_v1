from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),  # URL containing the item id will return our add_to_bag view and will be named add_to_bag
]
