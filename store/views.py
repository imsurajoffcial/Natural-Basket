from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,UserInfoForm
from django import forms

# Create your views here.

def category(request,foo):
    #replce with hyphens and spaces
     foo = foo.replace('-',' ')
     #grab the category from the url
     try:
         #look up the category
         category = Category.objects.get(name=foo)
         products = Product.objects.filter(category=category)
         return render(request,'category.html', {'products':products, 'category':category})
     except:
         messages.success(request,("that category doesn't exist"))
         return redirect('index')
     
     
     
def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def index(request):
    products = Product.objects.all
    return render(request,'index.html',{'products':products})


def about(request):
    return render(request,'about.html',{})


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('index')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out!"))
	return redirect('index')


def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect('index')
            else:
                messages.error(request, "There was an issue logging in. Please try again.")
                return redirect('login')
        else:
            messages.error(request, "There was a problem registering. Please correct the errors below.")
    return render(request, 'register.html', {'form': form})

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('index')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('index')

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(name__icontains =searched)
        
        if not searched:
            messages.success(request, "Sorry that product doesn't exists!")
            return render(request, "search.html",{'searched':searched})
        else:
            return render(request, "search.html",{'searched':searched})

    else:
     return render(request, "search.html")

    
