from django.conf.urls import url
from cadastral_map.views import AteCreateView, AteList, AteDelete, StreetCreateView, StreetList, ate_details, \
    street_details, StreetDelete, AddressCreateView, AddressList, address_details, AddressDelete, \
    ate_search_form, ate_search, street_search_form, street_search, address_search_form, address_search, MainPageView

urlpatterns = [
    url(r'^ate/$', AteCreateView.as_view(), name='create_ate'),
    url(r'^ate/list/$', AteList.as_view(), name='list_ate'),
    url(r'^ate/details/(?P<pk>\d+)', ate_details, name='details_ate'),
    url(r'^ate/delete/(?P<pk>\d+)', AteDelete.as_view(), name='delete_ate'),
    url(r'^ate/search-form/$', ate_search_form, name='search_ate'),
    url(r'^ate/search/$', ate_search, name='ate_search'),
    url(r'^street/$', StreetCreateView.as_view(), name='create_street'),
    url(r'^street/list/$', StreetList.as_view(), name='list_street'),
    url(r'^street/details/(?P<pk>\d+)', street_details, name='details_street'),
    url(r'^street/delete/(?P<pk>\d+)', StreetDelete.as_view(), name='delete_street'),
    url(r'^street/search-form/$', street_search_form, name='search_street'),
    url(r'^street/search/$', street_search, name='street_search'),
    url(r'^address/$', AddressCreateView.as_view(), name='create_address'),
    url(r'^address/list/$', AddressList.as_view(), name='list_address'),
    url(r'^address/details/(?P<pk>\d+)', address_details, name='details_address'),
    url(r'^address/delete/(?P<pk>\d+)', AddressDelete.as_view(), name='delete_address'),
    url(r'^address/search-form/$', address_search_form, name='search_address'),
    url(r'^address/search/$', address_search, name='address_search'),
    url(r'^$', MainPageView.as_view(), name='map'),

    ]
