from django.urls import path
from .views import Deleteapi,Updateapi,Detailapi,Createapi,create_place,update_place_view,delete_place_view



urlpatterns=[path('api/create', Createapi.as_view(), name='create_list'),  # List + Create
    path('api/<int:pk>/details', Detailapi.as_view(), name='detail'),  # Retrieve
    path('api/<int:pk>/update/', Updateapi.as_view(), name='update'),  # Update
    path('api/<int:pk>/delete', Deleteapi.as_view(), name='delete'), 
    path('update/<int:pk>/', update_place_view, name='update-place-form'),
    path('', create_place, name='create-place'),
    path('places-form/delete/<int:pk>/', delete_place_view, name='delete-place-form'),

]  