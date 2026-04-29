from django.shortcuts import render,redirect

# Create your views here.

from .forms import CustomUserCreationForm

from django.contrib.auth import login

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log in the user and redirect to home.
            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

