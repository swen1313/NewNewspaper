from django.urls import path

from .views import PostList, PostDetail, PostDeleteView, PostUpdateView, PostCreateView, PostSearchList

urlpatterns = [
    path('news', PostList.as_view(), name='news'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/add', PostCreateView.as_view(), name='news_add'),
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
    path('news/search', PostSearchList.as_view(), name='news_search'),
]