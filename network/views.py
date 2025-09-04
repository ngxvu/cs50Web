import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post,Follow
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"page_obj": page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "")
        if content.strip():
            Post.objects.create(author=request.user, content=content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/newpost.html", {
                "message": "Post content cannot be empty."
            })
    return render(request, "network/newpost.html")

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by("-timestamp")
    followers_count = Follow.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    is_following = Follow.objects.filter(follower=request.user, user=user).exists()

    return render(request, "network/profile.html", {
        "profile_user": user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })

@login_required
def following(request):
    # Get the users the current user is following
    following_users = User.objects.filter(followers__follower=request.user)
    # Filter posts by those users
    posts = Post.objects.filter(author__in=following_users).order_by("-timestamp")
    # Add pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"page_obj": page_obj})

@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(id=post_id, author=request.user)
            data = json.loads(request.body)
            content = data.get("content", "").strip()
            if content:
                post.content = content
                post.save()
                return JsonResponse({"message": "Post updated successfully."}, status=200)
            else:
                return JsonResponse({"error": "Content cannot be empty."}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found or unauthorized."}, status=404)
    return JsonResponse({"error": "PUT request required."}, status=400)
