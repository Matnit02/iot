from django.views.generic import TemplateView


class TempMapView(TemplateView):
    template_name = 'map.html'


class TempTableView(TemplateView):
    template_name = 'table.html'