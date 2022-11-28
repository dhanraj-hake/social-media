from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to = "profiles", default="default.png")
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username



class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    image = models.ImageField(upload_to="posts", default="defaultpost.png")
    description = models.CharField(max_length=250)
    likes = models.IntegerField(default=0)
    post_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username


class Like(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=20)

    def __str__(self):
        post = Post.objects.get(id=self.post_id)
        return "Like by "+ self.username+" " +post.description[0:10] +" Posted : "+post.username


class Followers(models.Model):

    following_by = models.CharField(max_length=20)
    following_to_user = models.CharField(max_length=20)

    def __str__(self):
        return self.following_by


