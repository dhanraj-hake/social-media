from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import Profile, Post, Like, Followers
from django.contrib.auth import login , logout, authenticate 
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random

# Create your views here.

# @login_required(login_url="/login")
def index(request):

    if request.user.is_anonymous:
        return redirect("/login")
    
    user_profile = Profile.objects.get(user=request.user)

    following_user_list = Followers.objects.filter(following_by=request.user.username)
    posts = []

    for user_obj in following_user_list:
        following_user_post = Post.objects.filter(username=user_obj.following_to_user)
        posts += following_user_post

    posts.sort(key= lambda obj : int("-"+str(obj.id)))
    
    params = {
        "posts" : posts,
        "user_profile" : user_profile
    }

    return render(request, "index.html", params)



def user_login(request):
    
    if not request.user.is_anonymous:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username = username , password=password)
        print(user)
        if user:
            login(request, user)
            print("Login User")
            return redirect("/")
        else:
            messages.info(request, "Username or Password Incorrect")
            return redirect("/login")

    return render(request, "login.html")



def user_signup(request):

    if not request.user.is_anonymous:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        print(username, email, password, password2)

        if password != password2:
            messages.info(request, "Password not match")
            return redirect("/signup")
        
        if password == password2:

            if len(password)<=6:
                messages.info(request, "Enter 8 Charactor Password")
                return redirect("/signup")

            if User.objects.filter(username=username).exists():
                messages.info(request,"Username taken")
                return redirect("/signup")

            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("/signup")

            # Create User
            user = User.objects.create_user(username = username, password=password, email=email)

            # login User
            auth_user = authenticate(username =username, password=password)
            login(request, auth_user)

            # Create Profile for User
            user_profile = Profile.objects.create(user=user, name=username)

            return redirect("/")

    return render(request, "signup.html")


def user_logout(request):

    logout(request)

    return redirect("/login")




def setting(request):
    
    if request.user.is_anonymous:
        return redirect("/login")

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        if request.FILES.get("image") == None:
            profile.profile_image = profile.profile_image
            profile.name = request.POST.get("name")
            profile.bio = request.POST.get("bio")
            profile.gender = request.POST.get("gender")
            profile.birth_date = request.POST.get("birthdate")
            profile.address = request.POST.get("address")

        if request.FILES.get("image") != None:
            profile.profile_image = request.FILES.get("image")
            profile.name = request.POST.get("name")
            profile.bio = request.POST.get("bio")
            profile.gender = request.POST.get("gender")
            profile.birth_date = request.POST.get("birthdate")
            profile.address = request.POST.get("address")
            
        profile.save()
    


    params = {
        "profile" : profile,
        "birthdate" : str(profile.birth_date),
        "user_profile" : profile
    }

    return render(request, "setting.html", params)



def create_post(request):

    print(request.user.is_anonymous)
    if request.user.is_anonymous:
        return redirect("/login")

    if request.method == "POST":

        if request.FILES.get("image") == None:
            desc = request.POST.get("desc")
            post = Post.objects.create(user=user, username = request.user.username,descriptio=desc,post_date=datetime.now())
        
        if request.FILES.get("image") != None:
            image = request.FILES.get("image")
            desc = request.POST.get("desc")
            post = Post.objects.create(user= request.user, username = request.user.username,image=image , description =desc,post_date=datetime.now())
            return redirect("/")
        


    return render(request, "createpost.html")


def like(request, id):

    if request.user.is_anonymous:
        return redirect("/login")

    try:

        liked_by_user = Like.objects.filter(post_id=id, username=request.user.username).first()
        post = Post.objects.get(id=id)
        
        if liked_by_user == None:
            new_like = Like.objects.create(post_id=id, username=request.user.username)
            post.likes = post.likes+1
        else:
            post.likes = post.likes-1
            liked_by_user.delete()
        post.save()

        postdetail = request.GET.get("postdetail")
        
        if postdetail:
            return redirect(f"/postdetail/{id}")

    except Exception as e:
        return redirect("/")

    return redirect("/")


def profile(request, username):

    if request.user.is_anonymous:
        return redirect("/login")

    user = User.objects.filter(username=username).first()

    if user == None:
        return redirect("/")

    profile = Profile.objects.filter(user=user).first()

    if profile == None:
        return redirect("/")

    posts = Post.objects.filter(username=username)
    
    post_count = len(posts)

    following_count = len(Followers.objects.filter(following_by=username))
    followers_count = len(Followers.objects.filter(following_to_user =username))

    if Followers.objects.filter(following_by=request.user.username, following_to_user=username).first():
        print(Followers.objects.filter(following_by=request.user.username).first())
        button_text = "Unfollow"
    else:
        button_text = "Follow"


    params = {
        "user" : user,
        "profile" : profile,
        "posts":posts,
        "post_count" : post_count,
        "following_count" : following_count,
        "followers_count" : followers_count,
        "button_text" : button_text,
        "user_profile" : profile
    }

    return render(request,"profile.html", params)




def follow_user(request):

    if request.method == "POST":
        following_by = request.POST.get("following_by")
        following_to_user = request.POST.get("following_to")

        is_following = Followers.objects.filter(following_by=following_by, following_to_user= following_to_user).first()

        if is_following:
            is_following.delete()
            return redirect(f"/profile/{following_to_user}")
        else:
            Followers.objects.create(following_by=following_by, following_to_user= following_to_user)
            return redirect(f"/profile/{following_to_user}")


    return redirect("/")    


def search(request):

    if request.user.is_anonymous:
        return redirect("/login")

    user_profile = Profile.objects.get(user=request.user)

    search = request.GET.get("search")

    user_list = User.objects.filter(username__icontains=search)

    profile_list = Profile.objects.filter(name__icontains=search)

    for user in user_list:
        profile_obj = Profile.objects.filter(user=user)
        profile_list.union(profile_obj)


    params = {
        "user_profile" : user_profile,
        "user_profile_list" : profile_list
    }

    return render(request ,"search.html", params)



def post_detail(request, id):

    if request.user.is_anonymous:
        return redirect("/login")
    
    user_profile = Profile.objects.get(user=request.user)

    post = Post.objects.filter(id=id).first()

    if post == None:
        return redirect("/")
    
    params = {
        "post" : post,
        "user_profile" : user_profile
    }
    return render(request, "post-detail.html", params)


def friends(request):

    if request.user.is_anonymous:
        return redirect("/login")

    user_profile = Profile.objects.get(user=request.user)

    all_user = User.objects.all()
    all_user = all_user.exclude(username=request.user.username)


    following_users = Followers.objects.filter(following_by=request.user.username)

    for i in following_users:
        all_user = all_user.exclude(username=i.following_to_user)
    
    print(all_user)
    all_user = list(all_user)
    random.shuffle(all_user)
    print(all_user)
    all_user = all_user

    all_profiles = []

    for i in all_user:
        profile = Profile.objects.filter(user=i).first()
        if profile:
            all_profiles.append(profile)
        if len(all_profiles) >=10:
            break
    

    params = {
        "all_profiles" : all_profiles,
        "user_profile" : user_profile
    }


    return render(request, "friends.html", params)

