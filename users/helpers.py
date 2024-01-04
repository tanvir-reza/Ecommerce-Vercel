from django.contrib import messages
from django.shortcuts import redirect
from users.models import Profile
from django.contrib.auth.models import User

def userProfileComplete(request):
    user = Profile.objects.filter(user=request.user).first()
    if user.name == "":
        messages.error(request, 'Please Update Your Profile')
        return redirect('update_profile')
    if user.phone == "":
        messages.error(request, 'Please Update Your Profile')
        return redirect('update_profile')
    if user.Shipping_address == "":
        messages.error(request, 'Please Update Your Profile')
        return redirect('update_profile')
    
