from functools import wraps
import jdatetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from sms.sms import send_sms
from .models import *
import time as t

request_counts = {}


class CreateChatView(View):
    def get(self, request):
        if not request.user.is_authenticated and request.user.is_staff:
            return redirect('index')
        if request.user.is_staff:
            messages.error(request, 'ادمین اجازه ایجاد چت ندارد')
            return redirect('dashboard')
        if Chat.objects.filter(user=request.user).exists():
            return redirect('chat', request.user.phone)
        else:
            Chat.objects.create(user=request.user)
            return redirect('chat', request.user.phone)


class ChatListView(View):
    def get(self, request):
        if request.user.is_staff:
            chats = Chat.objects.order_by('-updated_at').order_by('is_replied')
            return render(request, 'ticket_app/chat.html', {'chats': chats})
        else:
            return redirect('index')

    def post(self, request):
        if request.user.is_staff:
            phone = request.POST.get('phone')
            user = get_object_or_404(User, phone=phone)
            user_chat = Chat.objects.get(user=user)
            chats = Chat.objects.order_by('-updated_at')
            return render(request, 'ticket_app/chat.html', {'user_chat': user_chat, 'chats': chats})
        else:
            return redirect('index')


class ChatView(View):
    def post(self, request, phone):
        if not request.user.is_authenticated:
            return redirect('user_login')
        user = get_object_or_404(User, phone=phone)
        if not Chat.objects.filter(user=user).exists():
            messages.error(request, 'شما چت فعالی ندارید')
            return redirect('dashboard')
        if not request.user.phone == phone and not request.user.is_staff:
            return redirect('dashboard')
        user_text = request.POST.get('text')
        user_file = request.FILES.get('file')
        if not user_text and not user_file:
            messages.error(request, 'شما نمیتوانید پیام خالی ارسال کنید')
            return redirect('chat', phone)
        time_now = jdatetime.datetime.now()
        message_send_time = str(
            f'{time_now.time().hour}:{time_now.time().minute} {time_now.date().year}/{time_now.date().month}/{time_now.date().day}')
        if request.user.is_staff:
            if user_file:
                if user_file.size / 1000000 > 2:
                    messages.error(request, 'حجم فایل باید حداکثر دو مگابایت باشد')
                    return redirect(reverse('chat_list') + f'?phone={phone}')
                if str(user_file).split('.')[-1] not in ['jpg', 'png', 'webp', 'jpeg']:
                    messages.error(request, 'فرمت فایل باید jpg,png یا webp باشد')
                    return redirect(reverse('chat_list') + f'?phone={phone}')
                orginal_file_path = f'media/files/{user_file}'
                with open(orginal_file_path, 'wb+') as f:
                    for chunk in user_file.chunks():
                        f.write(chunk)

                user_dict = {"role": "admin", "content": f"/media/files/{user_file.name}", "type": "file",
                             "time": message_send_time}
            else:
                user_dict = {"role": "admin", "content": user_text, "type": "text", "time": message_send_time}
            object = Chat.objects.get(user=user)
            user_messages = object.messages_history
            user_messages.append(user_dict)
            object.is_replied = True
            object.save()
            send_sms(user.phone, 'userticket', parm1=user.fullname)
            return redirect(reverse('chat_list') + f'?phone={phone}')
        else:
            if user_file:
                if user_file.size / 1000000 > 2:
                    messages.error(request, 'حجم فایل باید حداکثر دو مگابایت باشد')
                    return redirect('chat', phone)
                elif str(user_file).split('.')[-1] not in ['jpg', 'png', 'webp', 'jpeg']:
                    messages.error(request, 'فرمت فایل باید jpg,png یا webp باشد')
                    return redirect('chat', phone)
                orginal_file_path = f'media/files/{user_file}'
                with open(orginal_file_path, 'wb+') as f:
                    for chunk in user_file.chunks():
                        f.write(chunk)
                user_dict = {"role": "user", "content": f"/media/files/{user_file.name}", "type": "file",
                             "time": message_send_time}
            else:
                user_dict = {"role": "user", "content": user_text, "type": "text", "time": message_send_time}
            object = Chat.objects.get(user_id=user.id)
            user_messages = object.messages_history
            user_messages.append(user_dict)
            object.is_replied = False
            object.save()
            send_sms('09120993133', 'adminticket', parm1=user.fullname)
            return redirect('chat', user.phone)

    def get(self, request, phone):
        if not request.user.is_authenticated:
            return redirect('user_login')
        user = get_object_or_404(User, phone=phone)
        if not Chat.objects.filter(user=user).exists():
            messages.error(request, 'شما چت فعالی ندارید')
            return redirect('dashboard')
        object = Chat.objects.get(user_id=user.id)
        return render(request, 'ticket_app/chat.html', {'user': user, 'chat': object})


def remove_chat(request, pk):
    if request.user.is_staff:
        if Chat.objects.filter(user__phone=pk).exists():
            Chat.objects.get(user__phone=pk).delete()
            messages.success(request, 'چت با موفیقیت حذف شد')
            return redirect('accounts:dashboard')
        messages.error(request, 'چت موردنظر یافت نشد')
        return redirect('accounts:dashboard')
    else:
        return redirect('accounts:home')


class AdminClearChat(View):
    def get(self, request, pk):
        if request.user.is_staff:
            chat = get_object_or_404(Chat, id=pk)
            chat.messages_history.clear()
            chat.is_replied = False
            chat.save()
            messages.success(request, 'چت پاکسازی شد')
            return redirect('chat_list')
        else:
            return redirect('index')
