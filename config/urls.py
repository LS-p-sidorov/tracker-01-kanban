from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from boards import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.board_list, name="board_list"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="boards/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("boards/new/", views.board_create, name="board_create"),
    path("boards/<int:pk>/", views.board_detail, name="board_detail"),
    path("boards/<int:pk>/tasks/new/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/move/", views.task_move, name="task_move"),
    path("users/", views.user_list, name="user_list"),
]
