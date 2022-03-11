from email import message
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Fairytale
from .forms import (
    AddFairytaleForm,
    LoginForm,
    SearchForm,
    ProfileUpdateForm,
    CategoryForm,
    CommentForm,
)
from django.db.models import Q
from django.utils.translation import gettext as _


def index(request):
    return render(request, "fairytales/index.html")

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
                messages.success(request, _(f"Hi {user.username}, you have been logged in."))
                return redirect("/fairytales")
            else:
                messages.warning(request, _("Login failed."))
        else:
            messages.warning(request, _("Login failed."))
    else:
        form = LoginForm()
    context = {"form": form, "success_message": success_message}
    return render(request, "fairytales/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("/fairytales")


# profile
@login_required
def profile(request):
    success_message = ""
    if request.method == "POST":
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if p_form.is_valid():
            p_form.save()
            success_message = f"Your account has been updated!"
            return redirect("profile") 

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"p_form": p_form, "success_message": success_message}

    return render(request, "fairytales/profile.html", context)

# overview
def collection(request):
    collection_list = Fairytale.objects.all().order_by("-id")
    paginator = Paginator(collection_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"collection_list": collection_list, "page_obj": page_obj}
    return render(
        request,
        "fairytales/collection.html", context
    )

# fairytale
def fairytale(request, slug):
    fairytale = Fairytale.objects.get(slug=slug)
    context = {"fairytale": fairytale}
    return render(request, "fairytales/fairytale.html", context)

@login_required
def add_fairytale(request):
    form = None
    if request.method == "POST":
        fairytale = Fairytale(posted_by=request.user)
        form = AddFairytaleForm(request.POST, request.FILES, instance=fairytale)
        is_valid = form.is_valid()
        if is_valid:
            form.save()
            messages.success(request,"Your fairytale has been saved.")
            return redirect("/fairytales")
        else:
            messages.warning(request, "The form needs fixes.")
    else:
        form = AddFairytaleForm()
    context = {"form": form}
    return render(request, "fairytales/add_fairytale.html", context)

@login_required
def update_fairytale(request, id):
    form = None
    fairytale = get_object_or_404(Fairytale, id=id)
    form = AddFairytaleForm(request.POST or None, instance=fairytale)
    if form.is_valid():
        form.save()
        messages.success(request, "You have successfully updated the fairytale.")
        return redirect("/fairytales")
    context = {"form": form, "fairytale": fairytale}
    return render(request, "fairytales/update_fairytale.html", context)

@login_required
def delete_fairytale(request, id):
    fairytale = get_object_or_404(Fairytale, id=id)
    if request.method == "POST":
        fairytale.delete()
        return redirect("/fairytales")

    return render(request, "fairytales/delete_fairytale.html")


# category
def CategoryView(request, cats):
    category_entries = Fairytale.objects.filter(category=cats)
    context = {"category_entries": category_entries, "cats": cats}
    return render(request, "fairytales/categories.html", context)

@login_required
def add_category(request):
    form = None
    if request.method == "POST":
        form = CategoryForm(request.POST)
        is_valid = form.is_valid()
        if is_valid:
            form.save()
            messages.success(request, "Your new category has been saved.")
            return redirect("/fairytales")
        else:
            messages.warning(request, "The form needs fixes.")
    else:
        form = CategoryForm()
    context = {"form": form}
    return render(request, "fairytales/add_category.html", context)


# comment
def add_comment(request, pk):
    form = None
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        is_valid = form.is_valid()
        if is_valid:
            fairytale = get_object_or_404(Fairytale, pk=pk)
            comment = form.save(commit=False)
            comment.fairytale = fairytale
            comment.save()
            messages.success(request,"Your comment has been saved.")
            return redirect(f"/fairytales/collection")
        else:
            messages.warning(request, "The form needs fixes.")
    else:
        form = CommentForm(initial={"name": request.user})

    context = {"form": form}
    return render(request, "fairytales/add_comment.html", context)


# search
def search(request):
    success_message = ""
    search_results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        is_valid = form.is_valid()
        if is_valid:
            search_term = request.GET["query"]
            search_results = Fairytale.objects.filter(
                Q(title__icontains=search_term)
                | Q(body__icontains=search_term)
                | Q(author__icontains=search_term)
            )
            if search_results:
                success_message = f'Fairytales matching "{search_term}":'
            else:
                success_message = f"No results for {search_term}."
        else:
            success_message = "Form needs fixes!"
    else:
        form = SearchForm()
    context = {
        "form": form,
        "success_message": success_message,
        "search_results": search_results,
    }
    return render(request, "fairytales/search.html", context)



