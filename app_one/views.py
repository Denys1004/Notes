from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.db.models import Q
from django.contrib import messages


# Welcome Page
#***********************************************************************
def index(request):	
    return render(request, 'welcome.html')	
# Home
#***********************************************************************
def home(request):	
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        users_posts = user.posts.all()
        users_themes = user.themes.all()
        context = {
            'all_posts': users_posts,
            'all_themes': users_themes,
            'user' : user,
            "page_title": 'Home'
        }
    return render(request, 'home.html', context)	

# Register
#***********************************************************************
def register(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            request.session.clear()
        return render(request, "register.html")
    else:
        request.session.clear()
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        errors = User.objects.validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/')
        new_user = User.objects.register(request.POST)
        request.session.clear()
        request.session['user_id'] = new_user.id
        request.session['initials'] = new_user.first_name[0].upper() + new_user.last_name[0].upper()
        return redirect('/home/')


# Login
#***********************************************************************
def login(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            request.session.clear()
        return render(request, "login.html")
    else:
        result = User.objects.authenticate(request.POST['email'],request.POST['password']) # Checking login
        if result == False:
            messages.error(request, "Email or password do not match.")
            return redirect('/')
        else:
            request.session.clear()
            user = User.objects.get(email = request.POST['email'])
            request.session['user_id'] = user.id
            request.session['initials'] = user.first_name[0].upper() + user.last_name[0].upper()
            return redirect('/home/')


# Logout
#***********************************************************************
def logout(request):
    request.session.clear()
    return redirect("/")    


# Search
#***********************************************************************
def search(request):
    zapros = request.GET['zapros']
    if zapros != '':
        user = User.objects.get(id = request.session['user_id'])
        users_posts = user.posts.all()
        users_themes = user.themes.all()
        result = users_posts.filter( Q(title__icontains=zapros) | Q(content__icontains=zapros) )
        context = {
            'post_results': result,
            'zapros': zapros,
             'all_posts': users_posts,
            'all_themes': users_themes,
            "page_title": 'Result'
        }
        return render(request, 'search_result.html', context)
    else:
        return redirect('/home/')


# Create Theme on Home Page
#***********************************************************************
def create_theme(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    Theme.objects.create(name = request.POST['name'], poster = cur_user)
    return redirect ('/home/')


# Go to the Theme to see posts
#***********************************************************************
def theme(request, theme_id):
    needed_theme = Theme.objects.get(id = theme_id)
    # all_posts = needed_theme.posts.all()
    user = User.objects.get(id = request.session['user_id'])
    theme_posts = needed_theme.posts.all()
    users_themes = user.themes.all()
    context = {
        'theme': needed_theme,
        'all_themes': users_themes,
        'all_posts' : theme_posts,
        "page_title": needed_theme.name
    }
    return render(request,'theme.html', context )


# Delete Theme 
#***********************************************************************
def delete_theme(request, theme_id):
    needed_theme = Theme.objects.get(id = theme_id)
    needed_theme.delete()
    return redirect('/home/')



# Create Post
#***********************************************************************
def create_post(request):
    cur_user = User.objects.get(id = request.session['user_id'])
    needed_theme = Theme.objects.get(id = request.POST['theme'])
    if request.POST['editordata']=="":
        return redirect(f'/theme/{needed_theme.id}/')
    elif request.POST['title'] == "":
        if needed_theme.posts.all():
            last_post = needed_theme.posts.count()
            num = last_post + 1
        else:
            num = 1
        Post.objects.create(title = f"Note {num}",  content = request.POST['editordata'], theme = needed_theme, poster = cur_user)
    else: 
        Post.objects.create(title = request.POST['title'], content = request.POST['editordata'], theme = needed_theme, poster = cur_user)
    return redirect(f'/theme/{needed_theme.id}/')


# Delete Post
#***********************************************************************
def delete_post(request, post_id):
    to_delete = Post.objects.get(id = post_id)
    theme = to_delete.theme
    to_delete.delete()
    return redirect(f'/theme/{theme.id}/')



# Edit Post
#***********************************************************************
def edit_post(request, post_id):
    needed_post = Post.objects.get(id = post_id)
    needed_theme = Theme.objects.get(id = needed_post.theme.id)
    user = User.objects.get(id = request.session['user_id'])
    users_posts = user.posts.all()
    users_themes = user.themes.all()
    if request.method == "GET":	
        context = {
            'needed_post': needed_post,
            'all_themes': users_themes,
            "page_title": "Edit"
        }
        return render(request, "edit_post.html", context)
    else:
        needed_post.title = request.POST['title']
        needed_post.content = request.POST['editordata']
        needed_post.save()
        return redirect(f'/theme/{needed_theme.id}/')