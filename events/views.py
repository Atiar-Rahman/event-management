from django.utils import timezone
from django.shortcuts import render
from events.models import Event,Participant,Category
from django.db.models import Q,Count
from .forms import EventForm, ParticipantForm, CategoryForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


def home(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    events=events[:9]
    return render(request,'events/home.html',{'events':events})



def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()

    # Search by name or location
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)

    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    # event = Event.objects.all()

    return render(request, 'events/event_detail.html', {'event': event})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


def event_update(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


def event_delete(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def dashboard(request):
    today = timezone.now().date()
    events = Event.objects.select_related('category').prefetch_related('participants').all()


    print(events)
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    total_categoris = Category.objects.count() 

    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()

    todays_events = Event.objects.filter(date=today).select_related('category').prefetch_related('participants')

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events_count,
        'past_events': past_events_count,
        'todays_events': todays_events,
        'events':events,
        'total_categoris':total_categoris
    }
    return render(request, 'events/dashboard.html', context)
