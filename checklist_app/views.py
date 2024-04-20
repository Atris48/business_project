from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from checklist_app.forms import ChecklistForm
from order_app.models import Order
from sms.sms import send_sms


class ChecklistView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, tracking_code=pk)
            if order.is_paid == False:
                messages.error(request, 'ابتدا صورت حساب خود را پرداخت کنید')
                return redirect('order_detail')
            form = ChecklistForm(instance=order.checklist)
            if request.user == order.user and order.is_paid or request.user.is_staff:
                return render(request, 'dashboard_app/checklist/checklist.html', {'form': form})
            else:
                return redirect('index')
        else:
            return redirect('login')


class ChecklistAdmin(View):
    def get(self, request, pk):
        if not request.user.is_staff:
            return redirect('index')
        order = get_object_or_404(Order, tracking_code=pk)
        if order.is_paid == False:
            messages.error(request, 'صورت حساب مورد نظر پرداخت نشده است')
            return redirect('dashboard')
        form = ChecklistForm(instance=order.checklist)
        return render(request, 'dashboard_app/checklist/admin_checklist.html', {'form': form})

    def post(self, request, pk):
        if not request.user.is_staff:
            return redirect('index')
        order = get_object_or_404(Order, tracking_code=pk)
        if order.is_paid == False:
            messages.error(request, 'صورت حساب مورد نظر پرداخت نشده است')
            return redirect('dashboard')
        form = ChecklistForm(request.POST, instance=order.checklist)
        if form.is_valid():
            form.save()
            send_sms(order.user.phone, 'firststage', parm1=order.user.fullname)
            messages.success(request, 'چک لیست مورد نظر آپدیت شد')
            return redirect('admin_order_list')
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نمیباشد')
            return redirect('update_checklist', pk)
