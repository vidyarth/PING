from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import Roomform
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = room.count()
    return render(request,"base/home.html",{
        "room" : room,
        "topic":topics,
        "room_count":room_count,
    })

def room(request,pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by("created")
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room",pk=room.id)
    return render(request,"base/room.html",{
        "room" : room,
        "room_messages" : room_messages,
        "participants" : participants,
    })

@login_required(login_url="login")
def create_room(request):
    form = Roomform
    if (request.method == "POST"):
        form = Roomform(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect("home")

    context = {'form':form}
    return render(request,"base/room_form.html",context)

@login_required(login_url="login")
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed here !")
    if (request.method == "POST"):
        form = Roomform(request.POST, instance=room)
        if (form.is_valid()):
            form.save()
            return redirect("home")
    context = {'form': form}
    return render(request,"base/room_form.html",context)


@login_required(login_url="login")
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here !")
    if (request.method == "POST"):
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", 
    {
        'obj' : room
    })


def loginpage(request):
    # if request.user.is_authenticated():
    #     return redirect("home")
    page = "login"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist !")   
        user = authenticate(request,username=username,password=password)
        #return HttpResponse(password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, "User invalid !")

    context = {"page" : page}
    return render(request,"base/login.html",context)

def logoutpage(request):
    logout(request)
    return redirect("home")

def register(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")

        else:
            messages.error(request,"An error occured during registration !")

    context = {"page" : page, "form" : form}
    return render(request,"base/login.html",context)