from django.contrib.gis.forms import OSMWidget
from cadastral_map.models import Ate, Streets, Address
from django.contrib.gis.forms import ModelForm


class AteForm(ModelForm):

    class Meta:
        model = Ate
        exclude = ['user', 'data_ate']
        widgets = {
            'geog': OSMWidget(attrs={'map_width': 1200, 'map_height': 650, 'default_lon': 24.37, 'default_lat': 52.20,
                                     'default_zoom': 10}),

        }


class StreetForm(ModelForm):

    class Meta:
        model = Streets
        exclude = ['user', ]
        widgets = {
            'geog': OSMWidget(attrs={'map_width': 1200, 'map_height': 650, 'default_lon': 24.37, 'default_lat': 52.20,
                                     'default_zoom': 10}),

        }


class AddressForm(ModelForm):

    class Meta:
        model = Address
        exclude = ['user',]
        widgets = {
            'geog': OSMWidget(attrs={'map_width': 1200, 'map_height': 650, 'default_lon': 24.37, 'default_lat': 52.20,
                                     'default_zoom': 10}),

        }

