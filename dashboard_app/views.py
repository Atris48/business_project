from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from account_app.forms import EditUserProfile
from account_app.models import User


def dashboard(request):
    return render(request, 'dashboard_app/dashboard.html')


def profile(request, phone):
    user = get_object_or_404(User, phone=phone)
    return render(request, 'dashboard_app/profile/profile.html', {'user': user})


def edit_profile(request, phone):
    user = get_object_or_404(User, phone=phone)
    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print(form.cleaned_data.get('image'))
            form.save()
            messages.success(request, 'پروفایل شما ویرایش شد')
            return redirect('profile', phone)
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
            return redirect('edit_profile', phone)
    form = EditUserProfile(instance=user)
    return render(request, 'dashboard_app/profile/edit_profile.html', {'form': form, 'user': user})
