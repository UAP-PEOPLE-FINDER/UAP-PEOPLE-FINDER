from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "main"

urlpatterns = [
    path("signup", views.signup_request, name="signup"),
    path("", views.login_request, name="login"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("profile", views.profile_request, name="profile"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path(
        "password_reset_profile",
        views.password_reset_profile_request,
        name="password_reset_profile",
    ),
    path("search", views.search_request, name="search"),
    path("friends", views.friends, name="friends"),  
    path("received_requests", views.received_requests, name="received_requests"),
    path("sent_requests", views.sent_requests, name="sent_requests"),
    path("view_profile/<int:profile_id>", views.view_profile, name="view_profile"),
    path("room/<str:room_name>/", views.room, name="room"),
    path("notification", views.notification, name="notification"),
]
if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)