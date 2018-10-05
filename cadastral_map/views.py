# unicode: utf-8
from django.contrib import auth
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import fromstr
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from cadastral_map.forms import AteForm, StreetForm, AddressForm
from .models import Ate, Streets, Address, UserProfile, Gas, Water
from django.views.generic import TemplateView
import datetime
import json
import psycopg2


# Основная карта
class MainPageView(TemplateView):
    template_name = 'cadastral_map/index.html'


# Формы для отображения пространственных данных на карте
def address_view(request):
    redis_key = 'address'
    address = cache.get(redis_key)
    if not address:
        address = serialize('geojson', Address.objects.all())
        cache.set(redis_key, address)
    return HttpResponse(address, content_type='json')


def street_view(request):
    redis_key = 'srteet'
    street = cache.get(redis_key)
    if not street:
        street = serialize('geojson', Streets.objects.all())
        cache.set(redis_key, street)
    return HttpResponse(street, content_type='json')


def ate_view(request):
    redis_key = 'ate'
    ate = cache.get(redis_key)
    if not ate:
        ate = serialize('geojson', Ate.objects.all())
        cache.set(redis_key, ate)
    return HttpResponse(ate, content_type='json')


# Формы для населенных пунктов
class AteCreateView(FormView):
    template_name = 'ate/create.html'
    form_class = AteForm
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        adress_obj = form.save(commit=False)
        user = self.request.user
        adress_obj.user = UserProfile.objects.get(id=user.id)
        form.save()
        print(form.cleaned_data)
        return super().form_valid(form)


class AteList(ListView):
    template_name = 'ate/list.html'
    model = Ate
    paginate_by = 20
    ordering = 'name_ate'


def ate_details(request, pk):
    obj = get_object_or_404(Ate, id=pk)
    if request.method == "POST":
        form = AteForm(request.POST, instance=obj)
        if form.is_valid():
            adress_obj = form.save(commit=False)
            adress_obj.user = UserProfile.objects.get(id=auth.get_user(request).id)
            form.save()
            return redirect('list_ate')
    else:
        form = AteForm(instance=obj)
    return render(request, 'ate/details.html', {'form': form, 'obj': obj})


class AteDelete(DeleteView):
    model = Ate
    template_name = 'ate/delete.html'

    def get_success_url(self):
        return reverse_lazy('list_ate')


# Поиск населенных пунктов
def ate_search_form(request):
    return render_to_response('ate/search_form.html')


def ate_search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            ate = Ate.objects.filter(name_ate__icontains=q)
            ates = ate.order_by('name_ate')
            return render_to_response('ate/search_results.html',
            {'ates': ates, 'query': q})
    else:
        return render_to_response('ate/search_form.html', {'error': error})


# Формы для улиц
class StreetCreateView(FormView):
    template_name = 'ate/create.html'
    form_class = StreetForm
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        adress_obj = form.save(commit=False)
        user = self.request.user
        adress_obj.user = UserProfile.objects.get(id=user.id)
        form.save()
        print(form.cleaned_data)
        return super().form_valid(form)


class StreetList(ListView):
    template_name = 'street/list.html'
    model = Streets
    paginate_by = 20
    ordering = 'name_stree'


def street_details(request, pk):
    obj = get_object_or_404(Streets, id=pk)
    if request.method == "POST":
        form = StreetForm(request.POST, instance=obj)
        if form.is_valid():
            adress_obj = form.save(commit=False)
            adress_obj.user = UserProfile.objects.get(id=auth.get_user(request).id)
            form.save()
            return redirect('list_street')
    else:
        form = StreetForm(instance=obj)
    return render(request, 'street/details.html', {'form': form, 'obj': obj})


class StreetDelete(DeleteView):
    model = Streets
    template_name = 'street/delete.html'

    def get_success_url(self):
        return reverse_lazy('list_street')


# Поиск улиц
def street_search_form(request):
    return render_to_response('street/search_form.html')


def street_search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            street = Streets.objects.filter(name_stree__icontains=q)
            streets = street.order_by('name_stree')
            return render_to_response('street/search_results.html',
            {'streets': streets, 'query': q})
    else:
        return render_to_response('street/search_form.html', {'error': error})


# Формы для адресов
class AddressCreateView(FormView):
    template_name = 'ate/create.html'
    form_class = AddressForm
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        adress_obj = form.save(commit=False)
        user = self.request.user
        adress_obj.user = UserProfile.objects.get(id=user.id)
        form.save()
        print(form.cleaned_data)
        return super().form_valid(form)


class AddressList(ListView):
    template_name = 'address/list.html'
    model = Address
    paginate_by = 20


def address_details(request, pk):
    obj = get_object_or_404(Address, id=pk)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=obj)
        if form.is_valid():
            adress_obj = form.save(commit=False)
            adress_obj.user = UserProfile.objects.get(id=auth.get_user(request).id)
            form.save()
            return redirect('list_address')
        else:
            return 'Вы не авторизированы'
    else:
        form = AddressForm(instance=obj)
    return render(request, 'address/details.html', {'form': form, 'obj': obj})


class AddressDelete(DeleteView):
    model = Address
    template_name = 'address/delete.html'

    def get_success_url(self):
        return reverse_lazy('list_address')


# Поиск адресов
def address_search_form(request):
    return render_to_response('address/search_form.html')


def address_search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            street = Streets.objects.filter(name_stree__icontains=q)
            addresss = Address.objects.filter(id_street__incontains=street)
            return render_to_response('address/search_results.html',
            {'addresss': addresss, 'query': q})
    else:
        return render_to_response('address/search_form.html', {'error': error})


# Кадастровая карта
# def get_geojson_object(field_name, table_name):
#     conn = psycopg2.connect("dbname=postgis5 user=admin  password='admin'")
#     cur = conn.cursor()
#     cur.execute("SELECT ST_AsGeoJSON({0}) from {1}".format(field_name, table_name))
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#
#     all_coordinate_LIST = []
#     for i in rows:
#         coord_list = json.loads(i[0])['coordinates']
#         for a in coord_list:
#             all_coordinate_LIST.append(a)
#     geojson = json.loads(rows[0][0])
#     geojson['coordinates'] = all_coordinate_LIST
#     return geojson
#
#
# def getCoordinatesAsMultiPolygon(coordinates):
#     multipolygon = []
#     polygons = json.loads(coordinates)
#     for i in polygons:
#         multipolygon.append(fromstr(i))
#
#     return MultiPolygon(multipolygon)
#
#
# def edit_map(request):
#     if request.method == 'POST':
#         user = UserProfile.objects.get(id=auth.get_user(request).id)
#
#         if request.POST['gasCoordinates']:
#             gas_multipolygon = getCoordinatesAsMultiPolygon(request.POST['gasCoordinates'])
#             Gas.objects.create(id_user=user, data_gas=datetime.datetime.now(),
#                                gas_title='gas_title', gas_geometry=gas_multipolygon)
#
#         if request.POST['waterCoordinates']:
#             water_multipolygon = getCoordinatesAsMultiPolygon(request.POST['waterCoordinates'])
#             Water.objects.create(id_user=user, data_water=datetime.datetime.now(),
#                                water_title='water_title', water_geometry=water_multipolygon)
#
#     context = {'viewModel': {
#         'gasGeoJson': get_geojson_object('gas_geometry', 'cadastral_map_gas'),
#         'waterGeoJson': get_geojson_object('water_geometry', 'cadastral_map_water')
#     }}
#
#     return render(request, 'cadastral_map/edit_map.html', context)

