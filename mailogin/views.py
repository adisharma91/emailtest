from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import MyUser
from .forms import LoginForm,UserCreationForm
from django.contrib.auth import authenticate,login, logout


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

    return render(request,'index.html')


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
