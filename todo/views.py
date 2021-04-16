from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from django.contrib.auth import authenticate, login as auth_login, logout as dj_logout, update_session_auth_hash
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Item, UserProfile
from .forms import TODOform, UserForm, UserEditForm, UserProfileForm, PasswordForm


def index(request):
    my_user = request.user  # check which account is logged in and fetch all information about them
    form = TODOform()
    if request.user.is_superuser:
        all_items = Item.objects.order_by('id')
        all_users = User.objects.filter(is_superuser=False)
        context = {'users': all_users, 'my_user': my_user, 'form': form, 'items': all_items}
        return render(request, 'todo/admin_todo.html', {'context': context})
    else:
        all_items = Item.objects.filter(user=my_user)
        content = {'items': all_items, 'form': form, 'my_user': my_user}
        return render(request, 'todo/index.html', {'context': content})


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(username=User.objects.get(email=username), password=password)
        except:
            user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('todo_home')

        else:
            messages.info(request, 'Invalid Username or password')
    return render(request, 'todo/login.html')


def register(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

        else:
            # print(form.is_valid())  # form contains data and errors
            errs = form.errors
            print(form.errors)
            # messages.error(request, errs)
    return render(request, 'todo/register.html', {'form': form})


def logout(request):
    dj_logout(request)
    return redirect('login')


def edit_user(request):
    user = request.user  # get user instance
    user_id = request.user.id  # get logged in user id
    userForm = UserEditForm(instance=user)
    print(user.userprofile)
    if user.userprofile.profile_pic:
        profileForm = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    else:
        profileForm = UserProfileForm(request.POST, request.FILES)

    if request.method == 'POST':
        editForm = UserEditForm(request.POST, instance=user)

        if user.userprofile.profile_pic:  # if user already have image update or change the image,
            profileForm.save()  # user does not want to change image then leave this field
        else:
            if profileForm.is_valid():  # if user is new then add new image and check the form is valid or not
                image = request.FILES['profile_pic']
                upload_img = UserProfile(user_id=user_id, profile_pic=image)
                upload_img.save()
            else:
                print(profileForm.errors)  # if form is not valid print errors

        if editForm.is_valid():  # check user edit form is valid or not
            editForm.save()
        else:
            print(editForm.errors)
        return redirect('todo_home')

    context = {'user_form': userForm, 'profile_form': profileForm}
    return render(request, 'todo/user_edit.html', context)  # user profile update successful


@require_POST
def addTODO(request):
    user_id = request.user.id
    if request.method == "POST":
        form = TODOform(request.POST)
        # user_id = request.user.id
        # print(user_id)
        if form.is_valid():
            item = request.POST['field']
            new_item = Item(user_id=user_id, field=item)
            new_item.save()
        else:
            print(form.errors)
    return redirect('todo_home')


# def add_profile_pic(request):
#     editProfileForm = UserProfileForm()
#     context = {'profile_form': editProfileForm}
#     return render(request, 'todo/user_edit.html', context)


def add_admin_todo(request):
    if request.method == "POST":
        form = TODOform(request.POST)
        if form.is_valid():
            item = request.POST['field']
            print(item)
            user_id = request.POST['user_todo']
            print(user_id)
            # item = request.POST['field']
            new_item = Item(user_id=user_id, field=item)
            new_item.save()
            return redirect('todo_home')
            # print(item)

        else:
            print(form.errors)
    return render(request, "todo/admin_todo.html")


def deleteTodo(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('todo_home')


def editTodo(request, id):
    item = Item.objects.get(id=id)
    updateForm = TODOform(instance=item)
    if request.method == 'POST':
        updateForm = TODOform(request.POST, instance=item)
        if updateForm.is_valid():
            updateForm.save()
            return redirect('todo_home')
    return render(request, "todo/update.html", {'updateForm': updateForm})


def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'todo/change_password.html', {
        'form': form
    })
