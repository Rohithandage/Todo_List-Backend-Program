from django.urls import path
from .views import UserAuthView, TaskView

urlpatterns = [
    path('auth/<str:action>/', UserAuthView.as_view(), name='user_auth'),
    path('tasks/', TaskView.as_view(), name='tasks'),
]
