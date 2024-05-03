from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record
from .forms import SignUpForm, AddRecordForm


def home (request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, please try again...")
            return redirect('home')
    else:
        return render (request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user (request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render (request, 'register.html', {'form': form})
    return render (request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render (request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'You Must Be Logged In To View That Page')
        return redirect('home') 
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_customer = Record.objects.get(id=pk)
        delete_customer.delete()
        messages.success(request, 'Record Deleted Successfully')
        return redirect('home') 
    else: 
        messages.success(request, 'You Must Be Logged In To Delete Customers')
        return redirect('home') 
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully")
                return redirect('home')
        return render (request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'You Must Be Logged In To Create Records')
        return redirect('home') 
    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Successfully")
            return redirect('home')
        return render (request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You Must Be Logged In To Update Records')
        return redirect('home') 