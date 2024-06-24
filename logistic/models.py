from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    registerDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    executionDate = models.DateTimeField()
    place = models.CharField(max_length=200)
    progress = models.IntegerField()  # models.PositiveIntegerField()
    finishDate = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    completed = models.DateTimeField(null=True, blank=True)
    # Esto me relaciona esta tabla con la tabla de usuarios. Si quiero que cuando se elimine el usuario se elimine todo entonces uso (User, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # bitacora = models.#####() #en revision

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=500)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)


class Inquiry(models.Model):
    id = models.AutoField(primary_key=True)
    # Es para saber a que evento está relacionado
    eventName = models.ForeignKey(Event, on_delete=models.CASCADE, null = True)
    description = models.TextField()

class HistoricDeletedEvents(models.Model):
    id = models.AutoField(primary_key=True)
    registerDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    executionDate = models.DateTimeField()
    place = models.CharField(max_length=200)
    progress = models.IntegerField()  # en revision
    finishDate = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    completed = models.DateTimeField(null=True, blank=True)
    deleted = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
