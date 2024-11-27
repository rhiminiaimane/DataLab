from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home_page(request):
    return render(request, "home.html")

@login_required
def page1(request):
    return render (request, 'page1.html', {})

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("page1")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form":form}) 