from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, RegisterView
from .views import signup, home

urlpatterns = [
    path(r'^$', home, name='home'),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('accounts/signup/', signup, name='signup'),
    # SocialAuth branch changes
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/',
         TemplateView.as_view(template_name='profile.html')),
    # This urls we will need for allauth apirest responses
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('rest-auth/github/', GithubLogin.as_view(), name='github_login'),
]
