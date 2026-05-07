from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Product.objects.filter(category_id=category_id, is_active=True)
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'MANAGER'

class ProductCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

class ProductUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

class CategoryListView(LoginRequiredMixin, ManagerRequiredMixin, ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Category
    template_name = 'products/category_form.html'
    fields = ['name']
    success_url = reverse_lazy('products:category_list')
