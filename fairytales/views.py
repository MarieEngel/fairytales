from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required 
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Fairytale, Category
from .forms import AddFairytaleForm, LoginForm, SearchForm, ProfileUpdateForm, CategoryForm
from django.db.models import Q


# Create your views here.


def index(request):
    return render(request, "fairytales/index.html")


def collection(request):
    collection_list = Fairytale.objects.all().order_by("-id")
    paginator = Paginator(collection_list, 5) # show 5  fairytale titles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request, "fairytales/collection.html", {"collection_list": collection_list, 'page_obj': page_obj}
    )


def fairytale(request, slug):
    fairytale = Fairytale.objects.get(slug=slug)
    context = {"fairytale": fairytale}
    return render(request, "fairytales/fairytale.html", context)

def CategoryView(request, cats):
    category_entries = Fairytale.objects.filter(category=cats)
    context = {
        'category_entries': category_entries,
        'cats': cats

    }
    return render(request, "fairytales/categories.html", context)


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
        fairytale = Fairytale(posted_by=request.user)
        form = AddFairytaleForm(request.POST, request.FILES, instance=fairytale)
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

def update_fairytale(request, id):
    success_message = ""
    form = None
    fairytale = get_object_or_404(Fairytale, id = id)
    form = AddFairytaleForm(request.POST or None, instance = fairytale)
    if form.is_valid():
        form.save()
        return redirect("/fairytales")
    context = {
        "form": form,
        "success_message": success_message,
        "fairytale": fairytale
    }
    return render(request, "fairytales/update_fairytale.html", context)


def delete_fairytale(request, id):
    fairytale = get_object_or_404(Fairytale, id = id)
    if request.method =="POST":
        fairytale.delete()
        return redirect("/fairytales")

    return render(request, "fairytales/delete_fairytale.html")



def add_category(request):
    success_message = ""
    form = None
    if request.method == "POST":
        form= CategoryForm(request.POST)
        is_valid = form.is_valid()
        if is_valid:
            form.save()
            success_message = "Your new category has been saved."
            return redirect("/fairytales")
        else:
            success_message = "The form needs fixes."
    else:
        form = CategoryForm()
    context = {"form": form, "success_message": success_message}
    return render(request, "fairytales/add_category.html", context)


def search(request):
    success_message = ""
    search_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        is_valid = form.is_valid()
        if is_valid:
            search_term = request.GET['query']
            search_results = Fairytale.objects.filter(
                Q(title__icontains=search_term) | Q(body__icontains=search_term) | Q(author__icontains=search_term)
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


@login_required
def profile(request):
    success_message= ""
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            success_message=f'Your account has been updated!'
            return redirect('profile') # Redirect back to profile page

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form, "success_message": success_message
    }

    return render(request, 'fairytales/profile.html', context)

