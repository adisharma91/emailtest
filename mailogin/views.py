from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import LoginForm,UserCreationForm,ProjectForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from emaillogin import settings


# Create your views here.
def registeruser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)

        if MyUser.objects.filter(email=request.POST.get('email')).exists():
            return render(request, 'registration/signup.html', {'form': form, "error": "Email already Exists"})

        if form.is_valid():
            form.save()

            user = authenticate(email=request.POST['email'], password=request.POST['password1'])

            login(request, user)

            return HttpResponseRedirect('/')

        else:
            form = UserCreationForm(request.POST or None)

            return render(request, "register.html", {'form': form})

    else:
        form = UserCreationForm()

    return render(request, "register.html", {'form': form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():

            user = authenticate(email=request.POST['email'], password=request.POST['password'])

            if user is not None:

                if user.is_active:
                    login(request, user)

                    return HttpResponseRedirect('/')
        else:
            return render(request,'login.html',{'form': form, 'msg':'Username/Password Incorrect. Please Try Again !!'})
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context)


def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/')


def index(request):
    projects = Project.objects.all()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(by=request.user.first_name,
                                             name=form.cleaned_data['name'],
                                             startdate=form.cleaned_data['startdate'],
                                             endate=form.cleaned_data['endate']
                                             )
            project.save()

        return redirect('/')
    else:
        form = ProjectForm()

    return render(request,'index.html',{'frm':form, 'projects':projects})


@login_required(login_url=settings.LOGIN_URL)
def profile(request,id):
    if request.method == 'POST':
        user = MyUser.objects.get(id=id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.occupation = request.POST.get('occupation')
        user.address = request.POST.get('address')
        user.save()

        return redirect('/')
    else:
        return render(request, 'profile.html')


def apply(request,id):
    if request.method == 'POST':
        applied = Applied.objects.create(projectid_id=id,
                                         userid_id=request.user.id
                                         )
        applied.save()

        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False})




