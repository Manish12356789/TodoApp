import django_filters
from django_filters import DateFromToRangeFilter, ModelChoiceFilter, widgets
from .models import *
from django import forms



class ItemFilterAdmin(django_filters.FilterSet):
    fromDate = DateFromToRangeFilter(field_name='created_date', lookup_expr='gte', label='Select Date Ranges:',
     widget =  widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control user-select btn-block mr-4 ml-4',
        }) )
    # toDate = DateTimeFromToRangeFilter(field_name='created_date', lookup_expr='lte', label='To Date:', 
    # widget = widgets.RangeWidget(attrs={
    #         'class': 'form-control user-select btn-block',
    #     }) )
    user = ModelChoiceFilter(queryset = User.objects.filter(is_superuser=False))
    # widget = forms.Select(attrs={
    #     'class': 'form-control user-select btn-block',
    # })
    # )
    class Meta:
        model = Item
        fields = ['fromDate', 'user']



class ItemFilterUser(django_filters.FilterSet):
    fromDate = DateFromToRangeFilter(field_name='created_date', lookup_expr='gte', label='Select Date Ranges:',
     widget =  widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control user-select btn-block mr-4 ml-4',
        }) )
    class Meta:
        model = Item
        fields = ['fromDate']
