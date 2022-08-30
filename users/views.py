from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm 
# for checking login before going to profile page using login_required decorative
from django.contrib.auth.decorators import login_required

# for checking color of the image
from colorthief import ColorThief
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created Successfully ')
            return redirect('login')
    else:
        form = UserRegisterForm
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":

        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile )
    current_user = request.user
    user_list = Post.objects.filter(author=current_user)
    img_path = str(current_user.profile.image.url)
    imgurl =  str(Path(__file__).resolve().parent.parent)
    image_url = imgurl+img_path
    print(image_url)
    color_thief = ColorThief(image_url)

    dominant_color = color_thief.get_color(quality=1)
    color = '#%02x%02x%02x' % dominant_color
    print('#%02x%02x%02x' % dominant_color)

    context = {
        'user_list': user_list,
        'u_form': u_form,
        'p_form': p_form,
        'posts': user_list,
        'color': color
    }
    
    return render(request,'users/profile.html',context)

    

