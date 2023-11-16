import random
from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib import messages
from .models import Profile, Post, Likepost, FollowersCount , Notification , Comment
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash   # hi
from .forms import UsernameChangeForm
from django.db import transaction
from .forms import PostForm
from django.contrib.auth import get_user_model

from core import models

# Create your views here.



def register(request):
    # return HttpResponse('<h1> welcome  to social book </h1>')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2 :
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already in use')
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username is already in use')
                return redirect('register')
            else:
                user = User.objects.create_user(username= username ,email=email ,password=password)
                user.save()
                
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request, user_login)
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('index')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect("register") 
    else:
        return render(request,'signup.html')
    
        
def Login(request):
    if request.method == 'POST':
        usernames = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=usernames, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request , "invalid username or password")
            return redirect('login')
    else:
        return render(request, 'signin.html')
            

@login_required(login_url='login')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
        
    user_posts = Post.objects.filter(user=request.user.username)
    feed.append(user_posts)

    feed_list = list(chain(*feed))

    # User suggestion logic
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.filter(username=user.user).first()
        if user_list:
            user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in all_users if (x not in user_following_all)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in new_suggestions_list if (x not in current_user)]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})
def logout(request):
    auth.logout(request)
    return render(request, 'signin.html')





@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    username_form = UsernameChangeForm()
    
    if request.method == 'POST':
        if 'new_username' in request.POST:
            username_form = UsernameChangeForm(request.POST)
            if username_form.is_valid():
                new_username = username_form.cleaned_data['new_username']
                with transaction.atomic():
                    old_username = request.user.username
                    request.user.username = new_username
                    request.user.save()

                    # Update profile image, bio, and location
                    if request.FILES.get('image') is not None:
                        user_profile.profileimg = request.FILES.get('image')
                    if request.FILES.get('image1') is not None:
                        user_profile.profileimg2 = request.FILES.get('image1')
                    user_profile.bio = request.POST.get('bio', '')
                    user_profile.location = request.POST.get('location', '')
                    user_profile.save()
                    
                    # Handle other updates and notifications if applicable

                    # Update the session and authentication hash
                    update_session_auth_hash(request, request.user)
        else:
            # Handle other profile updates
            if request.FILES.get('image') is not None:
                user_profile.profileimg = request.FILES.get('image')
            if request.FILES.get('image1') is not None:
                user_profile.profileimg2 = request.FILES.get('image1')
            user_profile.bio = request.POST.get('bio', '')
            user_profile.location = request.POST.get('location', '')
            user_profile.save()
        
        return redirect('settings')
    
    return render(request, 'setting.html', {'user_profile': user_profile, 'username_form': username_form})


@login_required(login_url='login')
def post(request):
    return HttpResponse('<h1>Post</h1>')


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')
    
    
    
@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like = Likepost.objects.filter(post_id=post_id, username=username).first()

    if like is None:
        new_like = Likepost.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.likes = post.likes + 1
        post.save()

        # Only create a notification for the post owner
        if post.user != request.user:  # Avoid notifying yourself
            # Get the user object for the post owner
            post_owner = User.objects.get(username=post.user)

            notification = Notification(
                user=post_owner,  # Use the post owner's user instance here
                notification_type='Like',
                post=post,
                sender=request.user
            )
            notification.save()

    else:
        like.delete()
        post.likes = post.likes - 1
        post.save()

    return redirect('/')





@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
    
    
    
@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})




from uuid import UUID
@login_required(login_url='login')
def delete_post(request, post_id):
    try:
        # Get the post object
        post = Post.objects.get(id=post_id)
        
        # Check if the user is the owner of the post
        if post.user == request.user.username:
            # Delete the post
            post.delete()
            return redirect('index')
        else:
            # Handle the case where the user is not the owner of the post
            return HttpResponse("You are not authorized to delete this post.")
    except Post.DoesNotExist:
        # Handle the case where the post with the given post_id doesn't exist
        return HttpResponse("The post does not exist.")
    
    
@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user.username:
        return HttpResponse("You are not authorized to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if not request.FILES.get('image'):
                form.cleaned_data['image'] = post.image
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})



@login_required(login_url="login")
def notification(request):
    user_notification = Notification.objects.filter(user=request.user , is_read= False)
    return render(request, 'notifications.html', {'notifications': user_notification})


@login_required(login_url='login')
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, post=post, content=content)

    return render(request, 'view_post.html', {'post': post, 'comments': comments})

@login_required(login_url='login')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, post=post, content=content)

    return redirect('view_post', post_id=post.id)

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the owner of the comment
    if comment.user == request.user:
        comment.delete()
    
    return redirect('view_post', post_id=comment.post.id)

@login_required(login_url='login')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the owner of the comment
    if comment.user == request.user:
        if request.method == 'POST':
            comment.content = request.POST.get('content')
            comment.save()
            return redirect('view_post', post_id=comment.post.id)
    
    return render(request, 'edit_comment.html', {'comment': comment})