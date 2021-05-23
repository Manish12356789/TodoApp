from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from .forms import PasswordResetFormWithError, PasswordResetConfirmForm

urlpatterns = [
    path('', views.login, name='login'),
    path('todo/', login_required(views.index), name='todo_home'),
    path('add_admin_todo', views.add_admin_todo, name='add_admin_todo'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('add/', views.addTODO, name='add'),
    path('delete/<id>/', views.deleteTodo, name='delete'),
    path('edit/<id>/', views.editTodo, name='edit'),
    path('change_password/', views.change_password, name='change_password'),



    # password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=PasswordResetFormWithError), name='password_reset'),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(form_class=PasswordResetConfirmForm),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete')

]
