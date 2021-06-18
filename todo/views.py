from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login as auth_login, logout as dj_logout, update_session_auth_hash
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from .models import Item, UserProfile
from .forms import TODOform, StatusForm, UserForm, UserEditForm, UserProfileForm, PasswordForm, UserSelectForm
from .filter import ItemFilterAdmin, ItemFilterUser

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount


image_url = ""

# @receiver(user_signed_up)
@login_required
def index(request, **kwargs):
    my_user = request.user  # check which account is logged in and fetch all information about them
    form = TODOform()
    usf = UserSelectForm()
    filterForm = ItemFilterAdmin()
    global image_url

    # fb_uid = SocialAccount.objects.filter(user_id=request.user, provider='facebook')


    try:
        try:
            socialaccount_obj = SocialAccount.objects.filter(provider='facebook', user_id=my_user)
            image_url = socialaccount_obj[0].extra_data['picture']['data']['url']
        except:
            socialaccount_obj = SocialAccount.objects.filter(provider='google', user_id=my_user)
            image_url = socialaccount_obj[0].extra_data['picture']    
    except:
        if my_user.userprofile.profile_pic:
            image_url = my_user.userprofile.profile_pic.url
        else:
            image_url = "/todo/static/todo/images/default.jpg"            
 
                
    if request.user.is_superuser:
        all_users = User.objects.filter(is_superuser=False)
        if request.method == "POST":
            
            items = Item.objects.all()
            filterForm = ItemFilterAdmin(request.POST, queryset=items)
            item = filterForm.qs

            context = {'form': form, 'usf':usf, 'my_user': my_user, 'all_users': all_users, 'dateFilterForm': filterForm, 'filter_items': item}
            return render(request, 'todo/admin_todo.html', context)
        else:
            all_items = Item.objects.order_by('-created_date')
            page = request.GET.get('page', 1)
            paginator = Paginator(all_users, 2)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)

            except EmptyPage:
                users = paginator.page(paginator.num_pages)

            context = {'users': users, 'all_users': all_users, 'my_user': my_user, 'form': form, 'usf':usf, 'dateFilterForm': filterForm, 'items': all_items}
            return render(request, 'todo/admin_todo.html', context)
    else:
        if request.method == "POST":

            items = Item.objects.filter(user=my_user)
            filterForm = ItemFilterUser(request.POST, queryset=items)
            item = filterForm.qs

            context = {'form': form, 'my_user': my_user, 'dateFilterForm': ItemFilterUser, 'filter_items': item}
            return render(request, 'todo/user_todo.html', context)
        else:
            all_items = Item.objects.filter(user=my_user).order_by('-created_date')
            page = request.GET.get('page', 1)
            paginator = Paginator(all_items, 5)
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)

            except EmptyPage:
                items = paginator.page(paginator.num_pages)

            # form1 = TODOform()
            context = {'items': items, 'my_user': my_user, 'dateFilterForm': ItemFilterUser, 'form': form, 'image_url': image_url}
            return render(request, 'todo/user_todo.html', context)
        
        
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

@login_required
def logout(request):
    dj_logout(request)
    return redirect('login')


@login_required
def edit_user(request):
    global image_url
    user = request.user  # get user instance
    user_id = request.user.id  # get logged in user id
    userForm = UserEditForm(instance=user)
    # print(user.userprofile)
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
            return redirect('todo_home')
        else:
            print(editForm.errors)
        

    context = {'user_form': userForm, 'profile_form': profileForm, 'image_url': image_url}
    return render(request, 'todo/user_edit.html', context)  # user profile update successful


@login_required
@require_POST
def addTODO(request):
    user_id = request.user.id
    if request.method == "POST":
        form = TODOform(request.POST)
        if form.is_valid():
            item = request.POST['field']
            new_item = Item(user_id=user_id, field=item)
            new_item.save()
        else:
            print(form.errors)
            messages.error(request, "** You must enter your task. **")
    return redirect('todo_home')


@login_required
def add_admin_todo(request):
    if request.method == "POST":
        form = TODOform(request.POST)
        usf = UserSelectForm(request.POST)
        if form.is_valid() and usf.is_valid:            
            user_id = request.POST['users']
            item = request.POST['field']
            new_item = Item(user_id=user_id, field=item)
            new_item.save()
        else:
            print(form.errors)
            print(usf.errors)
            # messages.error(request, "Must have to choose user.")
        return redirect('todo_home')
    # form = TODOform()
    # usf = UserSelectForm()
    # context = {'form': form, 'usf':usf}
    # return render(request, "todo/admin_todo.html")


@login_required
def deleteTodo(request, id):
    item = Item.objects.get(id=id)
    if request.method == "POST":
        item.delete()
        return redirect('todo_home')
    return render(request, 'modal.html', {'item':item})


@login_required
def editTodo(request, id):
    item = Item.objects.get(id=id)
    SForm = StatusForm(instance=item)
    updateForm = TODOform(instance=item)
    if request.method == 'POST':
        updateForm = TODOform(request.POST, instance=item)
        SForm = StatusForm(request.POST, instance=item)
        if updateForm.is_valid() and SForm.is_valid():
            updateForm.save()
            SForm.save()
            return redirect('todo_home')
    return render(request, "todo/update.html", {'updateForm': updateForm, 'statusform': SForm })


@login_required
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
        'password_change_form': form
    })


