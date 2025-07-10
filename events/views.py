from django.utils import timezone
from django.shortcuts import render
from events.models import Event,Participant,Category
from django.db.models import Q,Count
from .forms import EventForm, ParticipantForm, CategoryForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test,permission_required
# Create your views here.

def is_user(user):
    return user.groups.filter(name='user').exists()

def is_organizer(user):
    return user.groups.filter(name='organizer').exists()

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

@permission_required('events.add_event',login_url='no-permession')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@permission_required('events.change_event',login_url='no-permession')
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

@permission_required('events.delete_event',login_url='no-permession')
def event_delete(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@permission_required('events.add_event',login_url='no-permession')
def dashboard(request):
    type = request.GET.get('type', 'all')  

    today = timezone.now().date()

   
    counts = {
        'events': Event.objects.aggregate(
            total=Count('id'),
            upcoming=Count('id', filter=Q(date__gte=today)),
            past=Count('id', filter=Q(date__lt=today)),
        ),
        'participants': Participant.objects.aggregate(total=Count('id')),
        'categories': Category.objects.aggregate(total=Count('id')),
    }

    
    event_query = Event.objects.select_related('category').prefetch_related('participants')
    participant_query = Participant.objects.all()
    category_query = Category.objects.all()

  
    data = None
    data_type = ''

    if type == 'events':
        data = event_query.all()
        data_type = 'events'

    elif type == 'upcoming':
        data = event_query.filter(date__gte=today)
        data_type = 'upcoming_events'

    elif type == 'past':
        data = event_query.filter(date__lt=today)
        data_type = 'past_events'

    elif type == 'participants':
        data = participant_query
        data_type = 'participants'

    elif type == 'categories':
        data = category_query
        data_type = 'categories'

    else:
        data = event_query.all()
        data_type = 'events'  

    context = {
        'counts': counts,
        'data': data,
        'data_type': data_type,
    }

    return render(request, 'events/dashboard.html', context)





def participant_list(request):
   participants = Participant.objects.prefetch_related('events').all()
   return render(request, 'events/participant_list.html', {'participants': participants})




def participant_detail(request, id):
   participant = Participant.objects.get(id=id)
   return render(request, 'events/participant_detail.html', {'participant': participant})




def participant_create(request):
   if request.method == 'POST':
       form = ParticipantForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('participant_list')
   else:
       form = ParticipantForm()
   return render(request, 'events/participant_form.html', {'form': form})




def participant_update(request, id):
   participant = Participant.objects.get(id=id)
   if request.method == 'POST':
       form = ParticipantForm(request.POST, instance=participant)
       if form.is_valid():
           form.save()
           return redirect('participant_list')
   else:
       form = ParticipantForm(instance=participant)
   return render(request, 'events/participant_form.html', {'form': form})




def participant_delete(request, id):
   participant = Participant.objects.get(id=id)
   if request.method == 'POST':
       participant.delete()
       return redirect('participant_list')
   return render(request, 'events/participant_confirm_delete.html', {'participant': participant})



def category_list(request):
   categories = Category.objects.annotate(event_count=Count('events'))
   return render(request, 'events/category_list.html', {'categories': categories})


def category_detail(request, id):
   category = Category.objects.get(id=id)
   return render(request, 'events/category_detail.html', {'category': category})



@permission_required('events.add_category',login_url='no-permession')
def category_create(request):
   if request.method == 'POST':
       form = CategoryForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('category_list')
   else:
       form = CategoryForm()
   return render(request, 'events/category_form.html', {'form': form})

@permission_required('events.change_category',login_url='no-permession')
def category_update(request, id):
   category = Category.objects.get(id=id)
   if request.method == 'POST':
       form = CategoryForm(request.POST, instance=category)
       if form.is_valid():
           form.save()
           return redirect('category_list')
   else:
       form = CategoryForm(instance=category)
   return render(request, 'events/category_form.html', {'form': form})


@permission_required('events.delete_category',login_url='no-permession')
def category_delete(request, id):
   category = Category.objects.get(id=id)
   if request.method == 'POST':
       category.delete()
       return redirect('category_list')
   return render(request, 'events/category_confirm_delete.html', {'category': category})

def no_permession(request):
    return render(request,'no_permession.html')