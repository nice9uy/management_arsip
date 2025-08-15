from datetime import datetime
# from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# from django.shortcuts import render, redirect, get_object_or_404
# from datetime import datetime

# from django.urls import reverse
# from accounts.models import User
# from django.db import transaction
# from django.contrib.auth.decorators import login_required

# from asgiref.sync import sync_to_async
# from django.core.paginator import Paginator
import secrets
import string
# import time

# from django.db.models import Q
# import bleach
# from django.template.loader import render_to_string
from django.utils.html import strip_tags
from management_arsip.settings import copyright
# from django.db.models.functions import Length



def secure_random_string(length=15):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def clean_input(input_str):
    cleaned = strip_tags(input_str)
    return cleaned.strip()


def login_view(request):
    tahun_sekarang = datetime.now().year

    get_copyright = copyright

    context = {
        "page_title": "login",
        "tahun": tahun_sekarang,
        "get_copyright": get_copyright,
    }

    if request.method == "POST":
        username_login = clean_input(request.POST.get("nip", ""))
        password_login = clean_input(request.POST.get("password", ""))

        user = authenticate(
            request=request, nip=username_login, password=password_login
        )

        if user is not None:
            login(request, user)
            if password_login == "kemhan123":
                messages.warning(
                    request,
                    'Password Anda "kemhan123". Demi keamanan segera ganti Password!!!',
                )
                return redirect("dashboard")
            return redirect("dashboard")
        else:
            messages.error(request, "Periksa kembali NIP dan Password Anda benar!!!")
            return redirect("login")

    return render(request, "accounts/auth/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


def custom_404_view(request):
    return render(request, "404.html", status=404)
