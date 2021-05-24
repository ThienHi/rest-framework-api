from rest_framework.routers import DefaultRouter, SimpleRouter
from snippets.views import SnippetViewSet
from users.views import UserViewSet
from django.conf import settings


if settings.DEBUG:
    routers = DefaultRouter()
else:
    routers = SimpleRouter()

routers.register('snippets', SnippetViewSet)
routers.register('users', UserViewSet)
# routers.register('register', RegisterView)

app_name = 'api'
urlpatterns = routers.urls
