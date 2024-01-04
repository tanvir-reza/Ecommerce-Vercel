from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from cart.models import Order
from django.db.models import Sum
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        # print(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        username = username.lower()
        email = email.lower()
        username = username.strip()
        email = email.strip()
        username = username.replace(" ", "")
        if len(username) < 4:
            messages.error(request, 'Username must be 4 character long')
            return redirect('signup')
        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('signup')
        if len(password) < 6:
            messages.error(request, 'Password must be 6 character long')
            return redirect('signup')
        # print(username, email, password)
        exits = User.objects.filter(Q(username=username) | Q(email=email)).first()
        if exits is not None:
            messages.error(request, 'Username or Email Already Exists')
            return redirect('login')
        else:
            User.objects.create_user(username, email, password)
            messages.success(request, 'Account Created Successfully')
            return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        # print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Username or Password Incorrect')
            return redirect('login')
    return render(request, 'login.html')


@login_required(login_url='login')
def update_profile(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=request.user.profile, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Profile Update Failed')
            return redirect('update_profile')
    context = {
        'form':form,

        }
    return render(request, 'forms.html', context)

@login_required(login_url='login')
def dashboard(request):
    user = Profile.objects.filter(user=request.user).first()
    
    if user is not None:
        print("ami")
        if user.name == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
        if user.phone == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
        if user.Shipping_address == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')

    return render(request, 'dashboard.html')


@login_required(login_url='login')
def profile(request):
    user = Profile.objects.filter(user=request.user).first()
    
    if user is not None:
        print("ami")
        if user.name == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
        if user.phone == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
        if user.address == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')

    return render(request, 'profile.html')


@login_required(login_url='login')
def ordersView(request):
    oders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_orders = oders.count()
    print(f'Total:{total_orders}')
    total_delivered = oders.filter(payment_status=True).count()
    print(f'Delivered:{total_delivered}')
    total_pending = oders.filter(payment_status=False).count()
    total_spend = Order.objects.filter(user=request.user).aggregate(Sum('total_amount'))
    context = {
        'orders':oders,
        'total_orders':total_orders,
        'total_delivered':total_delivered,
        'total_pending':total_pending,
        'total_spend':total_spend,

    }
    return render(request, 'orders.html',context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')