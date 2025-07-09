from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import CustomRegistrationForm, LoginForm

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False  # Activate after email confirmation
            user.save()

            # Assign Participant group by default
            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)

            messages.success(request, "Account created. Please check your email to activate your account.")
            return redirect('sign-in')
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('dashboard_redirect')
            else:
                messages.error(request, "Account not activated. Please check your email.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'signin.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('sign-in')


@login_required
def dashboard_redirect(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    elif user.groups.filter(name='Organizer').exists():
        return redirect('organizer_dashboard')
    else:
        return redirect('participant_dashboard')
