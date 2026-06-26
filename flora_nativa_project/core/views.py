import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Planta, Region

PERENUAL_API_KEY = os.getenv("PERENUAL_API_KEY", "")


def home(request):
    region_id = request.GET.get("region")
    query = request.GET.get("q")

    plantas = Planta.objects.all()
    if region_id:
        plantas = plantas.filter(regiones__id=region_id)
    if query:
        plantas = plantas.filter(
            nombre_comun__icontains=query
        ) | plantas.filter(nombre_cientifico__icontains=query)

    regiones = Region.objects.all()
    return render(request, "index.html", {
        "plantas": plantas,
        "regiones": regiones,
        "query": query,
        "region_seleccionada": region_id,
    })


def detalle_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk)
    api_data = None

    if PERENUAL_API_KEY and (planta.perenual_id or planta.nombre_cientifico):
        try:
            if planta.perenual_id:
                url = (
                    f"https://perenual.com/api/species/details/"
                    f"{planta.perenual_id}?key={PERENUAL_API_KEY}"
                )
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    api_data = response.json()
            else:
                search_url = (
                    f"https://perenual.com/api/species-list?"
                    f"key={PERENUAL_API_KEY}&q={planta.nombre_cientifico}"
                )
                res = requests.get(search_url, timeout=5)
                if res.status_code == 200 and res.json().get("data"):
                    first_match = res.json()["data"][0]
                    planta.perenual_id = first_match.get("id")
                    planta.save()

                    detail_url = (
                        f"https://perenual.com/api/species/details/"
                        f"{planta.perenual_id}?key={PERENUAL_API_KEY}"
                    )
                    api_data = requests.get(detail_url, timeout=5).json()
        except requests.exceptions.RequestException:
            api_data = {"error": "No se pudo conectar con la API de Perenual en este momento."}

    return render(request, "detalle.html", {"planta": planta, "api_data": api_data})


def registro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registro.html", {"form": form})


def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_usuario(request):
    logout(request)
    return redirect("home")
