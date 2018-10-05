from django.conf.urls import url
from blog_app.views import article, addlike, addcomment, about, Articles

urlpatterns = [
    url(r'^articles/get/(?P<article_id>\d+)/$', view=article, name='article'),
    url(r'^articles/addlike/(?P<article_id>\d+)/$', view=addlike),
    url(r'^articles/addcomment/(?P<article_id>\d+)/$', view=addcomment, name='addcomment'),
    url(r'^about/$', view=about, name='about'),
    url(r'^', Articles.as_view(), name='articles'),


]
