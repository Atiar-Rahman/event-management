from django import forms
from events.models import Event, Category


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter event name', 'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter event description', 'class': 'w-full border rounded px-3 py-2', 'rows': 3}),
            'date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date', 'class': 'w-full border rounded px-3 py-2'}),
            'time': forms.TimeInput(attrs={'placeholder': 'HH:MM', 'type': 'time', 'class': 'w-full border rounded px-3 py-2'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter event location', 'class': 'w-full border rounded px-3 py-2'}),
            'category': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name', 'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter category description', 'class': 'w-full border rounded px-3 py-2', 'rows': 3}),
        }
