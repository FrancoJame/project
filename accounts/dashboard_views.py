from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from orders.models import OrderItem
from bookings.models import Booking, LoungeRoom
from products.models import Category

@staff_member_required
def admin_status_dashboard(request):
    # ... existing function logic ...
    sales_by_category = OrderItem.objects.values('product__category__name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')
    
    category_labels = [item['product__category__name'] for item in sales_by_category]
    category_data = [item['total_sold'] for item in sales_by_category]
    
    room_utilization = Booking.objects.values('room__name').annotate(
        booking_count=Count('id')
    ).order_by('-booking_count')
    
    room_labels = [item['room__name'] for item in room_utilization]
    room_data = [item['booking_count'] for item in room_utilization]
    
    context = {
        'title': 'Business Status Dashboard',
        'category_labels': category_labels,
        'category_data': category_data,
        'room_labels': room_labels,
        'room_data': room_data,
    }
    
    return render(request, 'admin/status.html', context)

class ManagerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/manager_dashboard.html'
    
    def test_func(self):
        return self.request.user.role == 'MANAGER'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Date filtering
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        order_items = OrderItem.objects.all()
        bookings = Booking.objects.all()
        
        if start_date:
            order_items = order_items.filter(order__created_at__date__gte=start_date)
            bookings = bookings.filter(created_at__date__gte=start_date)
        if end_date:
            order_items = order_items.filter(order__created_at__date__lte=end_date)
            bookings = bookings.filter(created_at__date__lte=end_date)
            
        context['start_date'] = start_date
        context['end_date'] = end_date

        # 1. Sales by Category
        sales_by_category = order_items.values('product__category__name').annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')
        
        context['category_labels'] = [item['product__category__name'] for item in sales_by_category]
        context['category_data'] = [item['total_sold'] for item in sales_by_category]
        
        # 2. Most Used Rooms
        room_utilization = bookings.values('room__name').annotate(
            booking_count=Count('id')
        ).order_by('-booking_count')
        
        context['room_labels'] = [item['room__name'] for item in room_utilization]
        context['room_data'] = [item['booking_count'] for item in room_utilization]
        
        # Summary Stats
        context['total_orders'] = order_items.aggregate(total=Sum('quantity'))['total'] or 0
        context['total_bookings'] = bookings.count()
        
        return context

