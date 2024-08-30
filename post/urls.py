from django.contrib import admin
from django.urls import path , include
from .views import ReadPostsView , ChangesPosts
urlpatterns =[
    path('posts/', ReadPostsView.as_view({'get': 'list'}), name = "list"),
    path('posts/create/', ChangesPosts.as_view({'post': 'create'}), name="create"),
    path('posts/<int:pk>/update',ChangesPosts.as_view({"patch":"update"}),name="update" ),
    path('posts/<int:pk>/delete/', ChangesPosts.as_view({"delete": "delete"}), name="delete") ,

]

