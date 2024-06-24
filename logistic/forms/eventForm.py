from django.forms import ModelForm, ValidationError
from django.forms import DateTimeInput
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from ..models import Event


class EventForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.all(), label="Usuario")

    class Meta:
        model = Event
        fields = ["name", "executionDate", "place",
                  "progress", "finishDate", "important", "user"]
        widgets = {
            'executionDate': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'finishDate': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        labels = {
            'name': 'Nombre',
            'executionDate': 'Fecha de Ejecución',
            'place': 'Lugar',
            'progress': 'Progreso',
            'finishDate': 'Fecha de Finalización',
            'important': 'Importante',
            'user': 'Usuario'
        }

    def clean_progress(self):
        progress = self.cleaned_data['progress']
        if progress < 0:
            raise ValidationError("No puede ser negativo.")
        elif progress > 100:
            raise ValidationError("No puede ser mayor a 100.")
        return progress

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['executionDate'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['finishDate'].input_formats = ('%Y-%m-%dT%H:%M',)
