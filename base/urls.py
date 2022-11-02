from django.urls import path,include
from .views import taskCreate, taskDelete, taskList,taskDetail, taskUpdate,LoginView,LogoutView

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',taskList.as_view(),name='home'),
    path('task/<int:pk>/',taskDetail.as_view(),name='task'),
    path('task-create/',taskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',taskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',taskDelete.as_view(),name='task-delete'),
    
]

