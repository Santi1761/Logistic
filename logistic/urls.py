from django.urls import path
from django.contrib import admin
from .views import task
from .views import event
from .views import user
from .views import feedback
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', user.home, name='home'),
    path('signup/', user.signup, name='signup'),
    path('logout/', user.signout, name='logout'),
    path('', user.signin, name='signin'),
    path('signin/', user.signin, name='signin'),
    path('event/checklist/<int:event_id>',
         event.event_checklist, name='event_checklist'),
    path('create/event/', event.create_event, name='create_event'),
    path('create/task/<event_id>/', task.create_task, name='create_task'),
    path('edit/event/<int:event_id>/', event.edit_event, name='edit_event'),
    path('edit/event/<int:event_id>/complete',
         event.complete_event, name='event_complete'),
    path('edit/event/<int:event_id>/delete',
         event.delete_event, name='event_delete'),
    path('home/search/', user.search_user, name='users_search'),
    path('home/profile', user.user_profile, name='user_profile'),
    path('edit/task/<int:task_id>/', task.edit_task, name='edit_task'),
    path('edit/task/<int:task_id>/delete',
         task.delete_task, name='task_delete'),
    path('forgot-password/', PasswordResetView.as_view(template_name='password_reset_form.html',
         email_template_name='password_reset.html'), name="password_reset"),
    path('forgot-password-done/', PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name="password_reset_done"),
    path('forgot-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('forgot-password/done/', PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('delete/user/', user.delete_user, name='delete_user'),
    path('home/calendar', event.events_calendar, name ='events_calendar'),
    path('feedback/', feedback.send_email_to_client, name = 'feedback'),
    path('historic_deleted_events/', event.historic_deleted_events,
         name='historic_deleted_events')

]
