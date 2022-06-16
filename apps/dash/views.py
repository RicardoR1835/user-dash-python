from multiprocessing import context
from urllib import response
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# the index function is called when root is visited
def index(request):
    return render(request, "dash/index.html")

def signin(request):
    return render(request, "dash/login.html")


def register(request):
    return render(request, "dash/register.html")

def new(request):
    isAdmin = User.objects.get(id=request.session['id'])
    if isAdmin.user_level != 9:
        messages.success(request, "Not Authorized to create a new user")
        return redirect('/dashboard')
    return render(request, "dash/add_user.html")

def login(request):
    user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
    print("*" * 80)
    print(user)

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signin')
    user = User.objects.get(email=request.POST['email'])
    request.session['id'] = user.id
    return redirect("/dashboard")

def dash(request):
    if 'id' not in request.session:
        messages.success(request, "Not logged in!")
        return redirect('/register')
    context = {
        "users": User.objects.all(),
        "logged_user": User.objects.get(id=request.session['id'])
    }
    return render(request, 'dash/dashboard.html', context)

def create(request):
    if "count" not in request.session:
        request.session['count'] = 0
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    if request.method == "POST":
        user = User.objects.create(first_name=request.POST['fn'], last_name=request.POST['ln'], email=request.POST['email'], password=request.POST['password'])
        if "id" not in request.session:
            request.session['id'] = user.id
        if request.session['count'] == 0:
            user.user_level = 9
            user.save()
        else:
            user.user_level = 1
            user.save()
        request.session['count'] += 1 
        return redirect('/dashboard')

def show(request, num):
    request.session['current_page'] = num
    context = {
        "user": User.objects.get(id=num),
        "messages": Message.objects.all(),
        "visitor": User.objects.get(id=request.session['id'])
    }
    return render(request, 'dash/show.html', context)

def edit(request, num):
    isAdmin = User.objects.get(id=request.session['id'])
    if isAdmin.user_level == 9 or int(isAdmin.id) == int(num):
        context = {
            "user": User.objects.get(id=num)
        }
        return render(request, "dash/edit_user.html", context)
    else:
        messages.success(request, "Not Authorized to edit")
        return redirect('/dashboard')

def update(request):
    print("in update")
    print(request.POST)
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/edit/{request.POST['id']}")
    user = User.objects.get(id=request.POST['id'])
    user.first_name = request.POST['fn']
    user.last_name = request.POST['ln']
    if user.email != request.POST['email']:
        print("email is not equal to post")
        email = User.objects.filter(email=request.POST['email'])

        if len(email) > 0:
            messages.error(request, "Email already exists")
            return redirect(f'/edit/{user.id}')
        else:
            user.email = request.POST['email']
            user.save()
    if request.POST['level'] != '0':
        user.user_level = request.POST['level']
    user.save()
    return redirect('/dashboard')

def updatepw(request):
    errors = User.objects.pw_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/edit/{request.POST['id']}")
    user = User.objects.get(id=request.POST['id'])
    user.password = request.POST['password']
    user.save()
    return redirect('/dashboard')

def destroy(request, num):
    user = User.objects.get(id=num)
    user.delete()
    return redirect('/dashboard')




def new_message(request):
    if request.method == "POST":
        msg_for = User.objects.get(id=request.POST['id'])
        msg_by = User.objects.get(id=request.session['id'])
        msg = Message.objects.create(message=request.POST['message'], created_by=msg_by, created_for=msg_for)
        return redirect(f'/show/{msg_for.id}')

def new_comment(request):
    if request.method == "POST":
        current_user_page = User.objects.get(id=request.POST['user_id'])
        comment_creator = User.objects.get(id=request.session['id'])
        msg = Message.objects.get(id=request.POST['msg_id'])
        comment = Comment.objects.create(comment=request.POST['comment'], message=msg, user=comment_creator)
        return redirect(f'/show/{current_user_page.id}')


def msg_like(request, num):
    current_page = request.session['current_page']
    msg = Message.objects.get(id=num)
    user_liking = User.objects.get(id=request.session['id'])
    msg.likes_on_messages.add(user_liking)
    msg.save()
    return redirect(f'/show/{current_page}')


def msg_unlike(request,num):
    current_page = request.session['current_page']
    msg = Message.objects.get(id=num)
    user_liking = User.objects.get(id=request.session['id'])
    msg.likes_on_messages.remove(user_liking)
    msg.save()
    return redirect(f'/show/{current_page}')

def cmnt_like(request, num):
    current_page = request.session['current_page']
    cmt = Comment.objects.get(id=num)
    user_liking = User.objects.get(id=request.session['id'])
    cmt.likes_on_comment.add(user_liking)
    cmt.save()
    return redirect(f'/show/{current_page}')

def cmnt_unlike(request,num):
    current_page = request.session['current_page']
    cmt = Comment.objects.get(id=num)
    user_liking = User.objects.get(id=request.session['id'])
    cmt.likes_on_comment.remove(user_liking)
    cmt.save()
    return redirect(f'/show/{current_page}')






def logout(request):
    del request.session['id']
    return redirect("/signin")