from django.urls import path
from .views import blog_list, blog_detail, toggle_like, toggle_star, toggle_bookmark

urlpatterns = [
    path('blogs/', blog_list),
    path('blogs/<int:pk>/', blog_detail),
    path('blogs/<int:pk>/like/', toggle_like),
    path('blogs/<int:pk>/star/', toggle_star),
    path('blogs/<int:pk>/bookmark/', toggle_bookmark),
]