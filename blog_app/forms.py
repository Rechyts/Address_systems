# -*- coding: utf-8 -*-
from django.contrib.gis.forms import OSMWidget
from django.forms import ModelForm

from blog_app.models import Comments, Article


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comments_text']


class ArticleGeoForm(ModelForm):

    class Meta:
        model = Article
        fields = ['geog']
        widgets = {
            'geog': OSMWidget(attrs={'map_width': 1200, 'map_height': 650, 'default_lon': 24.37, 'default_lat': 52.20,
                                     'default_zoom': 10}),
        }
