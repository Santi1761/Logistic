from django.test import TestCase
from django.forms import DateTimeInput
import logistic.forms
from logistic.forms.eventForm import EventForm
from logistic.forms.taskForm import TaskForm
from logistic.forms.taskForm import TaskChecklist
from logistic.forms.taskForm import TaskForm, TaskChecklist 


class forms_test(TestCase):
    def test_event_form_valid(self):
        form = EventForm(data={
            'name': 'Evento de prueba',
            'executionDate': '2022-12-31T23:59',
            'place': 'Lugar de prueba',
            'progress': 'Avance de prueba',
            'finishDate': '2023-01-01T00:01',
            'important': True,
            'user': 1,
        })
        self.assertFalse(form.is_valid())
        
    def test_event_form_invalid(self):
        form = EventForm(data={})
        self.assertFalse(form.is_valid())
        
    def test_task_checklist_form_valid(self):
        form = TaskChecklist(data={
            'done': True,
        })
        self.assertTrue(form.is_valid())
        
    def test_field_labels(self):
        event_form = EventForm()
        task_form = TaskForm()
        task_checklist_form = TaskChecklist()  


        self.assertEqual(event_form.fields['name'].label, 'Nombre')
        self.assertEqual(event_form.fields['executionDate'].label, 'Fecha de Ejecución')
        self.assertEqual(event_form.fields['place'].label, 'Lugar')
        self.assertEqual(event_form.fields['progress'].label, 'Progreso')
        self.assertEqual(event_form.fields['finishDate'].label, 'Fecha de Finalización')
        self.assertEqual(event_form.fields['important'].label, 'Importante')
        self.assertEqual(event_form.fields['user'].label, 'Usuario')
        
        self.assertEqual(task_form.fields['name'].label, 'Nombre')
        self.assertEqual(task_form.fields['event'].label, 'Evento')
        
        self.assertEqual(task_checklist_form.fields['done'].label, 'Hecho')
        
    def test_required_fields(self):
        event_form = EventForm(data={})
        task_form = TaskForm(data={})
        
        self.assertFalse(event_form.is_valid())
        self.assertIn('name', event_form.errors)
        self.assertIn('executionDate', event_form.errors)
        self.assertIn('place', event_form.errors)
        self.assertIn('finishDate', event_form.errors)
        self.assertIn('user', event_form.errors)
        
        self.assertFalse(task_form.is_valid())
        self.assertIn('name', task_form.errors)
        self.assertIn('event', task_form.errors)
        
    def test_date_time_format(self):
        event_form = EventForm()
        
        self.assertIsInstance(event_form.fields['executionDate'].widget, DateTimeInput)
        self.assertIsInstance(event_form.fields['finishDate'].widget, DateTimeInput)
        