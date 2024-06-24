from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from ..forms.taskForm import TaskForm
from ..models import Event
from ..models import Task
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse


def create_task(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'GET':
        form = TaskForm(event_instance=event)
        context = {'formForTask': form, 'event': event}
        return render(request, 'create_task.html', context)
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.event = event
            new_task.save()

            subject = 'Nueva tarea creada'
            message = f'Se ha creado una nueva tarea: {new_task.name}'
            from_email = 'your@example.com' 
            recipient_list = [request.user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print(f"Error al enviar correo electrónico: {e}")

            return redirect(reverse('event_checklist', args=[event_id]))
        else:
            context = {
                "formForTask": form,
                'error': 'Por favor, digite valores válidos',
                'event': event
            }
            return render(request, "create_task.html", context)


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'GET':
        if request.user.is_superuser:
            form = TaskForm(instance=task)
        else:
            user_events = Event.objects.filter(user=request.user)
            form = TaskForm(instance=task)
            form.fields['event'].queryset = user_events
    else:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not request.user.is_superuser:
                task.user = request.user
            task.save()

            subject = 'Tarea actualizada'
            message = f'Se ha actualizado la tarea: {task.name}'
            from_email = 'your@example.com'
            recipient_list = ['recipient@example.com']

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print(f"Error al enviar correo electrónico: {e}")

            return redirect('event_checklist', event_id=task.event.id)
        else:
            return render(request, "edit_task.html", {'taskId': task, 'form': form, 'error': "Error al intentar actualizar, intente de nuevo"})

    return render(request, "edit_task.html", {'taskId': task, 'form': form})


def delete_task(request, task_id):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=task_id)
    else:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('event_checklist', event_id=task.event.id)
