# unicode: utf-8
from django.conf.urls import url, include
from django.contrib.gis import admin
from blog_app.views import mainview
from cadastral_map.views import ate_view, street_view, address_view, edit_map
from django.conf import settings
from django.views.static import serve

admin.autodiscover()
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ate.data/', ate_view, name='ate'),
    url(r'^street.data/', street_view, name='street'),
    url(r'^address.data/', address_view, name='address'),
    url(r'^auth/', include('auth_app.urls')),
    url(r'^blog/', include('blog_app.urls')),
    url(r'^map/$', edit_map, name='edit_map'),
    url(r'^', include('cadastral_map.urls')),
    url(r'^mainview/', mainview),
]
