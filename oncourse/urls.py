from django.urls import path, include
from django.conf.urls import url
from . import views, admin

app_name = 'oncourse'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.view_profile, name="profile"),
    path('userslist/', views.UsersList, name="userslist"),
    url(r'^ajax/validate_username/$', views.validate_username),
]
