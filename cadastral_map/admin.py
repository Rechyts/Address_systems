# unicode: utf-8
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from cadastral_map.models import Gas, PropType, AteCategory, Region, \
    District, Selsovet, Ate, StreetCategory, Streets, Address, Water

admin.site.register(Ate, admin.OSMGeoAdmin)
admin.site.register(Streets, admin.OSMGeoAdmin)
admin.site.register(Address, admin.OSMGeoAdmin)
admin.site.register((PropType, AteCategory, Region, District, Selsovet, StreetCategory, Gas, Water))
