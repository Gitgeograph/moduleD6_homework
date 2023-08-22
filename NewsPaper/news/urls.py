from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostUpdateView, PostCreateView, PostDeleteView, upgrade_me, ProfileView, HomeView
from .views import PostCategoryView, subscribe_to_category, unsubscribe_to_category, CategoriesView

app_name = 'news'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/', PostList.as_view(), name='all_posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='postDetail'),
    path('news/search', PostSearch.as_view(), name='post_search' ),

    path('news/add', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('categories/', CategoriesView.as_view(), name='categories'),
    path('category/<int:pk>', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe_to_category, name='unsubscribe'),
    
]