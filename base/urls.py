from django.urls import path,include
from .views import taskList

urlpatterns = [
    path('',taskList.as_view(),name='home'),
]

