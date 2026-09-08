from django.contrib import admin
from django.urls import path, include
from task_manager import views as main_views
from users import views as user_views

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('', main_views.index, name='index'),
    path('users/', include('users.urls')),
    path('statuses/', include('statuses.urls')),
    path('tasks/', include('tasks.urls')),
    path('labels/', include('labels.urls')),
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    path('logout/', user_views.UserLogoutView.as_view(), name='logout'),
]
