from django.urls import path, include

app_name = 'accounts'  # namespace utama

urlpatterns = [
    path('', include('accounts.url.auth_urls', namespace='auth')),
    # path('', include('accounts.urls.profile_urls', namespace='profile')),
]