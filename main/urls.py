from django.urls import path

from main.apis import signup, login, profile

urlpatterns = [
    path('signup/', signup, name="user-signup"),
    path('login/', login, name="user-login"),
    path('profile/', profile, name="user-profile"),
]
