from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from events.models import Event, Category
from .forms import EventForm, CategoryForm
from django.contrib.auth import get_user_model
User = get_user_model()

# ---------------------------
# Helper decorator for groups
def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) or u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


# ---------------------------
def home(request):
    events = Event.objects.select_related('category').prefetch_related('rsvps').all()[:9]
    return render(request, 'events/home.html', {'events': events})

def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('rsvps').all()

    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))

    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, id):
    event = get_object_or_404(Event.objects.select_related('category').prefetch_related('rsvps'), id=id)
    return render(request, 'events/event_detail.html', {'event': event})

# ---------------------------
# Organizer & Admin only views

@group_required('Organizer', 'Admin')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@group_required('Organizer', 'Admin')
def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

@group_required('Organizer', 'Admin')
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# ---------------------------
# RSVP for Participants

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.rsvps.all():
        messages.info(request, "You have already RSVP'd for this event.")
    else:
        event.rsvps.add(user)
        messages.success(request, f"RSVP successful for event '{event.name}'.")
    return redirect('event_detail', id=event_id)

# ---------------------------
# Participant Dashboard

@login_required
def participant_dashboard(request):
    user = request.user
    rsvp_events = user.rsvp_events.select_related('category').all()
    return render(request, 'users/participant_dashboard.html', {'events': rsvp_events})

# ---------------------------
# Category Views

@group_required('Organizer', 'Admin')
def category_list(request):
    categories = Category.objects.annotate(event_count=Count('events'))
    return render(request, 'events/category_list.html', {'categories': categories})

@group_required('Organizer', 'Admin')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})

@group_required('Organizer', 'Admin')
def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form})

@group_required('Organizer', 'Admin')
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})

# ---------------------------
# Dashboard summary (Admin focused)

@group_required('Admin')
def dashboard(request):
    today = timezone.now().date()

    counts = {
        'events': Event.objects.aggregate(
            total=Count('id'),
            upcoming=Count('id', filter=Q(date__gte=today)),
            past=Count('id', filter=Q(date__lt=today)),
        ),
        'participants': User.objects.filter(groups__name='Participant').count(),
        'categories': Category.objects.count(),
    }

    events = Event.objects.select_related('category').all()
    categories = Category.objects.all()
    participants = User.objects.filter(groups__name='Participant').all()

    context = {
        'counts': counts,
        'events': events,
        'categories': categories,
        'participants': participants,
    }
    return render(request, 'events/dashboard.html', context)
