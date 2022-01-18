from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fairytale
from .forms import AddFairytaleForm, LoginForm, SearchForm
from django.db.models import Q

# Create your views here.


def index(request):
    return render(request, "fairytales/index.html")


def collection(request):
    collection_list = Fairytale.objects.all()
    return render(
        request, "fairytales/collection.html", {"collection_list": collection_list}
    )


def fairytale(request, slug):
    fairytale = Fairytale.objects.get(slug=slug)
    context = {"collection": fairytale}
    return render(request, "fairytales/fairytale.html", context)


def login_page(request):
    form = LoginForm()
    success_message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                success_message = f"Hi {user.username}, you have been logged in."
                return redirect('/fairytales')
            else:
                success_message = "Login failed."
        else:
            success_message = "Login failed."
    else:
        form = LoginForm()
    context = {"form": form, "success_message": success_message}
    return render(request, "fairytales/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("/fairytales")


def add_fairytale(request):
    success_message = ""
    form = None
    if request.method == "POST":
        form = AddFairytaleForm(request.POST, request.FILES)
        is_valid = form.is_valid()
        if is_valid:
            form.save()
            success_message = "Your fairytale has been saved."
            return redirect("/fairytales")
        else:
            success_message = "The form needs fixes."
    else:
        form = AddFairytaleForm()
    context = {"form": form, "success_message": success_message}
    return render(request, "fairytales/add_fairytale.html", context)


def search(request):
    success_message = ""
    search_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        is_valid = form.is_valid()
        if is_valid:
            search_term = request.GET['query']
            search_results = Fairytale.objects.filter(
                Q(title__icontains=search_term) | Q(body__icontains=search_term)
            )
            if search_results:
                success_message = f'Fairytales matching "{search_term}":'
            else:
                success_message = f"No results for {search_term}."
        else:
            success_message = "Form needs fixes!"
    else:
        form = SearchForm()
    context = {"form": form, "success_message": success_message, 'search_results': search_results}
    return render(request,"fairytales/search.html", context)



