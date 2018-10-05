# unicode: utf-8
from django.contrib.gis.db import models
from django.db.models import SET_NULL
from blog_app.models import UserProfile
from django.contrib.auth.models import User


class Gas(models.Model):
    id_user = models.ForeignKey(UserProfile, null=True)
    data_gas = models.DateField(auto_now_add=True, null=True)
    gas_title = models.CharField(max_length=20,null=True)
    gas_geometry = models.MultiPolygonField(null=True)


class Water(models.Model):
    id_user = models.ForeignKey(UserProfile, null=True)
    data_water = models.DateField(auto_now_add=True, null=True)
    water_title = models.CharField(max_length=20,null=True)
    water_geometry = models.MultiPolygonField(null=True)


class AteCategory(models.Model):
    name_category_ate = models.CharField(max_length=254,default=None)

    def __str__(self):
        return self.name_category_ate


class Region(models.Model):
    name_region = models.CharField(max_length=254, default=None)

    def __str__(self):
        return '{0} область'.format(self.name_region)


class District(models.Model):
    name_district = models.CharField(max_length=254, default=None)
    id_region = models.ForeignKey(Region)

    def get_district(self):
        return self.ate_set.all()

    def __str__(self):
        return '{0} район'.format(self.name_district)


class Selsovet(models.Model):
    name_ss = models.CharField(max_length=254, default=None)
    id_district = models.ForeignKey(District, default=True)

    def __str__(self):
        return '{0} сельсовет'.format(self.name_ss)


class Ate(models.Model):
    name_ate = models.CharField(max_length=254, verbose_name='Наименование населенного пункта')
    categor = models.ForeignKey(AteCategory, verbose_name='Категория')
    region = models.ForeignKey(Region, default=None, null=True, verbose_name='Область')
    distr = models.ForeignKey(District, SET_NULL, blank=True, null=True, verbose_name='Район')
    ss = models.ForeignKey(Selsovet, SET_NULL, null=True, blank=True, verbose_name='Сельсовет')
    data_ate = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, verbose_name='Пользователь')
    geog = models.MultiPolygonField(verbose_name='')

    class Meta:
        unique_together = (('name_ate', 'categor', 'region', 'distr', 'ss'),)

    def __str__(self):
        return '{0} {1}'.format(self.categor, self.name_ate)


class StreetCategory(models.Model):
    name_category_street = models.CharField(max_length=254, default=None)

    def __str__(self):
        return self.name_category_street


class Streets(models.Model):
    name_stree = models.CharField(max_length=254, default=None, verbose_name='Наименование элемента улично-дорожной сети')
    cat_street = models.ForeignKey(StreetCategory, verbose_name='Категория')
    id_ate = models.ForeignKey(Ate, verbose_name='Населенный пункт')
    user = models.ForeignKey(UserProfile, verbose_name='Пользователь')
    data_stree = models.DateField(auto_now_add=True)
    geog = models.MultiLineStringField(verbose_name='')

    class Meta:
        unique_together = (('name_stree', 'cat_street', 'id_ate'),)

    def __str__(self):
        return '{0} {1} {2}'.format(self.id_ate, self.cat_street, self.name_stree)


class PropType(models.Model):
    name_prop_type = models.CharField(max_length=254, default=None)

    def __str__(self):
        return self.name_prop_type


class Address(models.Model):
    prop_type = models.ForeignKey(PropType, verbose_name='Тип адреса')      # тип адреса: земельный участок или капитальное строение
    id_street = models.ForeignKey(Streets, default=None, null=True, verbose_name='Наименование улично-дорожной сети')
    house_num = models.SmallIntegerField(verbose_name='Номер дома')
    house_ind = models.CharField(max_length=2, blank=True, default=None, verbose_name='Индекс дома')
    corp_num = models.SmallIntegerField(null=True, blank=True, default=None, verbose_name='Номер корпуса')
    data_addr = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, verbose_name='Пользователь')
    geog = models.PointField(verbose_name='')

    class Meta:
        unique_together = (('prop_type', 'id_street', 'house_num', 'house_ind', 'corp_num'),)

    def __str__(self):
        return '{0} {1}'.format(self.id_street, self.house_num, self.house_ind, self.corp_num)

