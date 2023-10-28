from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def index(request):
    # return HttpResponse('<h1> welcome  to social book </h1>')
    return render(request,'index.html')


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
                return redirect('register')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request,'signup.html')
    
        
def Login(request):
    if request.method == 'POST':
        usernames = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=usernames, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/ATR')
        else:
            messages.info(request , "invalid username or password")
            return redirect('login')
    else:
        return render(request, 'signin.html')
            
        
        
        
def logout(request):
    auth.logout(request)
    return render(request, 'signin.html')



@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    
    return render(request, 'setting.html', {'user_profile': user_profile})
    