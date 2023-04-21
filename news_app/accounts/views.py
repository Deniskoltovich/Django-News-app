from django.shortcuts import render, redirect, reverse
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from news.views import list_publications


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(
                username = username,
                password = password
            )
            login(request, user)
            return redirect(reverse('list_publications'))
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'registration/register.html', context)
        
    
            

def logout_user(request):
    logout(request)
    return redirect(reverse('list_publications'))

