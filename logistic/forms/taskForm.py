from django.forms import ModelForm, HiddenInput
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from ..models import Task
from ..models import Event


class TaskForm(ModelForm):
    event = ModelChoiceField(queryset=Event.objects.all(), label="Evento")

    class Meta:
        model = Task
        fields = ["name", "event", "done"]
        labels = {
            'name': 'Nombre',
            'event': 'Evento',
            'done': 'Hecho',
        }

    def __init__(self, *args, **kwargs):
        # Recibe el evento como argumento adicional
        event_instance = kwargs.pop('event_instance', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        # Si se proporciona un evento, lo establece como inicial y lo hace oculto
        if event_instance:
            self.fields['event'].initial = event_instance
            self.fields['event'].widget = HiddenInput()


class TaskChecklist(ModelForm):
    class Meta:
        model = Task
        fields = ["done"]
        labels = {
            'done': 'Hecho',
        }
