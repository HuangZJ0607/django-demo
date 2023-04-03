from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('article-list/', views.article_list, name='article-list'),
    path('article-detail/<int:id>/', views.article_detail, name='article-detail'),
    path('article-create/', views.article_create, name='article-create'),
    path('article-delete/<int:id>/', views.article_delete, name='article-delete'),
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article-safe-delete'),
    path('article-update/<int:id>/', views.article_update, name='article-update'),
]
