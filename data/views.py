import pandas as pd
import numpy as np
from django.shortcuts import render
from django.views.generic import TemplateView
from .methods import csv_to_db
from .models import supermarket
from .charts import objects_to_df, Chart

PALETTE = ['#465b65', '#184c9c', '#d33035', '#ffc107', '#28a745', '#6f7f8c', '#6610f2', '#6e9fa5', '#fd7e14', '#e83e8c', '#17a2b8', '#6f42c1' ]

def error_500(request):
    return render(request,'500.html')
class Dashboard(TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):     
        context = super().get_context_data(**kwargs)
        
        df = objects_to_df(supermarket, date_cols=['%Y-%m', 'date'])

        
        context['charts'] = []

        
        city_payment_radar = Chart('radar', chart_id='city_payment_radar', palette=PALETTE)
        city_payment_radar.from_df(df, values='total', stacks=['payment'], labels=['city'])
        context['charts'].append(city_payment_radar.get_presentation())

        exp_polar = Chart('polarArea', chart_id='polar01', palette=PALETTE)
        exp_polar.from_df(df, values='total', labels=['payment'])
        context['charts'].append(exp_polar.get_presentation())

        exp_doughnut = Chart('doughnut', chart_id='doughnut01', palette=PALETTE)
        exp_doughnut.from_df(df, values='total', labels=['city'])
        context['charts'].append(exp_doughnut.get_presentation())

        exp_bar = Chart('bar', chart_id='bar01', palette=PALETTE)
        exp_bar.from_df(df, values='total', labels=['city'])
        context['charts'].append(exp_bar.get_presentation())

        city_payment = Chart('groupedBar', chart_id='city_payment', palette=PALETTE)
        city_payment.from_df(df, values='total', stacks=['payment'], labels=['date'])
        context['charts'].append(city_payment.get_presentation())

        city_payment_h = Chart('horizontalBar', chart_id='city_payment_h', palette=PALETTE)
        city_payment_h.from_df(df, values='total', stacks=['payment'], labels=['city'])
        context['charts'].append(city_payment_h.get_presentation())

        city_gender_h = Chart('stackedHorizontalBar', chart_id='city_gender_h', palette=PALETTE)
        city_gender_h.from_df(df, values='total', stacks=['gender'], labels=['city'])
        context['charts'].append(city_gender_h.get_presentation())

        city_gender = Chart('stackedBar', chart_id='city_gender', palette=PALETTE)
        city_gender.from_df(df, values='total', stacks=['gender'], labels=['city'])
        context['charts'].append(city_gender.get_presentation())

        return context
