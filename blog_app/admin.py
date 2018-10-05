from django.contrib.gis import admin
from django.contrib.gis.admin import GeoModelAdmin
from django.contrib.gis.admin.options import spherical_mercator_srid
from django.contrib.gis.gdal import HAS_GDAL
from django.core.exceptions import ImproperlyConfigured

from blog_app.models import UserProfile, Article

admin.site.register(UserProfile)


class OSMGeoAdmin(GeoModelAdmin):
    map_template = 'gis/admin/osm.html'
    num_zoom = 13
    map_srid = spherical_mercator_srid
    max_extent = '-20037508,-20037508,20037508,20037508'
    max_resolution = '156543.0339'
    point_zoom = num_zoom - 6
    units = 'm'

    fields = ['article_title', 'article_text', 'article_image', 'article_date', 'geog']
    list_filter = ['article_date']

    def __init__(self, *args):
        if not HAS_GDAL:
            raise ImproperlyConfigured("OSMGeoAdmin is not usable without GDAL libs installed")
        super(OSMGeoAdmin, self).__init__(*args)

admin.site.register(Article, OSMGeoAdmin)