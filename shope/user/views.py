from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Successfully created for {username}")
            return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', { 'form': form })
