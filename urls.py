from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',
    url(r'^anting/mkds/', TemplateView.as_view(template_name='anting/mkds.html')),
    url(r'^pythonflowvisualizer', views.python_flow_visualizer),
)