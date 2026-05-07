from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('add/', views.ProductCreateView.as_view(), name='product_add'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('category/all/', views.CategoryListView.as_view(), name='category_list'),
    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('category/<int:category_id>/', views.ProductListView.as_view(), name='product_list_by_category'),
]
