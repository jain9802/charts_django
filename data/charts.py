import random
import string
from dataclasses import dataclass, field
from typing import List
import pandas as pd
import numpy as np
import palettable

from palettable.lightbartlein.diverging import BlueDarkRed12_6 as palette

def objects_to_df(model, fields=None, exclude=None, date_cols=None, **kwargs):
    
    
    if not fields:
        fields = [field.name for field in model._meta.get_fields()]

    if exclude:
        fields = [field for field in fields if field not in exclude]

    records = model.objects.filter(**kwargs).values_list(*fields)
    df = pd.DataFrame(list(records), columns=fields)

    if date_cols:
        strftime = date_cols.pop(0)
        for date_col in date_cols:
            df[date_col] = df[date_col].apply(lambda x: x.strftime(strftime))
    
    return df

def get_random_colors(num, colors=[]):
    
    while len(colors) < num:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        if color not in colors:
            colors.append(color)

    return colors

def get_colors():
    
    try:
        return palette.hex_colors
    except:
        return get_random_colors(6)

def generate_chart_id():
    
    return ''.join(random.choice(string.ascii_letters) for i in range(8))

def get_options():
    
    return {}

@dataclass
class Chart:
    
    chart_type: str
    datasets: List = field(default_factory=list)
    labels: List = field(default_factory=list)
    chart_id: str = field(default_factory=generate_chart_id)
    palette: List = field(default_factory=get_colors)
    options: dict = field(default_factory=get_options)

    def from_lists(self, values, labels, stacks):
        
        self.datasets = []

        # make sure we have the right number of colors
        if len(self.palette) < len(values):
            get_random_colors(num=len(values), colors=self.palette)
        
        # build the datasets
        for i in range(len(stacks)):
            self.datasets.append(
                {
                    'label': stacks[i],
                    'backgroundColor': self.palette[i],
                    'data': values[i],
                }
            )

        if len(values) == 1:
            self.datasets[0]['backgroundColor'] = self.palette

        self.labels = labels

    def from_df(self, df, values, labels, stacks=None, aggfunc=np.sum, round_values=0, fill_value=0):
        
        pivot = pd.pivot_table(
            df,
            values=values,
            index=stacks,
            columns=labels,
            aggfunc=aggfunc,
            fill_value=0
        )

        pivot = pivot.round(round_values)
        
        values = pivot.values.tolist()
        labels = pivot.columns.tolist()
        stacks = pivot.index.tolist()

        self.from_lists(values, labels, stacks)
    
    def get_html(self):
        code = f'<canvas id="{self.chart_id}"></canvas>'
        return code

    def get_elements(self):
        elements = {
            'data': {
                'labels': self.labels, 
                'datasets': self.datasets
            },
            'options': self.options
        }

        if self.chart_type == 'stackedBar':
            elements['type'] = 'bar'
            self.options['scales'] = {
                        'xAxes': [
                            {'stacked': 'true'}
                        ], 
                        'yAxes': [
                            {'stacked': 'true'}
                        ]
                    }

        if self.chart_type == 'bar':
            elements['type'] = 'bar'
            self.options['scales'] = {
                        'xAxes': [
                            {
                                'ticks': {
                                    'beginAtZero': 'true'
                                }
                            }
                        ], 
                        'yAxes': [
                            {
                                'ticks': {
                                    'beginAtZero': 'true'
                                }
                            }
                        ]
                    }

        if self.chart_type == 'groupedBar':
            elements['type'] = 'bar'
            self.options['scales'] = {
                        'xAxes': [
                            {
                                'ticks': {
                                    'beginAtZero': 'true'
                                }
                            }
                        ], 
                        'yAxes': [
                            {
                                'ticks': {
                                    'beginAtZero': 'true'
                                }
                            }
                        ]
                    }
        
        if self.chart_type == 'horizontalBar':
            elements['type'] = 'horizontalBar'
            self.options['scales'] = {
                        'xAxes': [
                            {
                                'ticks': {
                                    'beginAtZero': 'true'
                                }
                            }
                        ], 
                        'yAxes': [
                            {
                                'ticks': {
                                    'beginAtZero': 'true'
                                }
                            }
                        ]
                    }

        if self.chart_type == 'stackedHorizontalBar':
            elements['type'] = 'horizontalBar'
            self.options['scales'] = {
                        'xAxes': [
                            {'stacked': 'true'}
                        ], 
                        'yAxes': [
                            {'stacked': 'true'}
                        ]
                    }

        if self.chart_type == 'doughnut':
            elements['type'] = 'doughnut'
        
        if self.chart_type == 'polarArea':
            elements['type'] = 'polarArea'
        
        if self.chart_type == 'radar':
            elements['type'] = 'radar'

        return elements
    
    def get_js(self):
        code = f"""
            var chartElement = document.getElementById('{self.chart_id}').getContext('2d');
            var {self.chart_id}Chart = new Chart(chartElement, {self.get_elements()})
        """
        return code

    def get_presentation(self):
        code = {
            'html':self.get_html(),
            'js': self.get_js(),
        }
        return code