from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm

def index(request):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
         'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
