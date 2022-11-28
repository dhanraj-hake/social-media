from django.urls import path
from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path("setting/", views.setting, name="setting"),
    path("createpost/", views.create_post, name="createpost"),
    path("like/<int:id>", views.like, name="like"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/", views.follow_user, name="followuser"),
    path("search/", views.search, name="search"),
    path("postdetail/<int:id>", views.post_detail, name="postdetail"),
    path("friends/", views.friends, name="friends"),
]
