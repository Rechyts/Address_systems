from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.gis.db import models


class UserProfile(User):
    orgname = models.CharField(max_length=200, verbose_name='Name of organization')
    birthday = models.DateField(verbose_name='Date of Birthday')

    def __str__(self):
        return self.username

MAX_TEXT_LENGTH = 500


class Article(models.Model):
    class Meta():
        db_table = 'article'

    article_title = models.CharField(max_length=200)
    article_text = models.TextField()
    article_image = models.ImageField(upload_to='images/', blank=True, null=True)
    article_date = models.DateTimeField()
    artticle_likes = models.IntegerField(default=0)
    article_comments = models.IntegerField(default=0)
    geog = models.PointField(verbose_name='Add marker')

    def __str__(self):
        return self.article_title

    def get_short_text(self):
        if len(self.article_text) > MAX_TEXT_LENGTH:
            return self.article_text[:MAX_TEXT_LENGTH]
        else:
            return self.article_text


class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField(verbose_name='Text of your comment')
    comments_article = models.ForeignKey(Article)
    comments_user = models.ForeignKey(User)
    comments_date = models.DateTimeField(auto_now_add=True)


class Likes(models.Model):
    class Meta():
        db_table = 'likes'

    likes_vote = models.IntegerField(default=1)
    likes_article = models.ForeignKey(Article)
    likes_user = models.ForeignKey(User)

    @classmethod
    def create(cls, article, user):
        like_object = cls(likes_article=article, likes_user=user)
        return like_object

