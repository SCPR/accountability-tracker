# coding=utf-8

from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q, Avg, Max, Min, Sum, Count
from maplight_finance.models import InitiativeContributor
#from bakery.views import BuildableListView, BuildableDetailView
import logging

#logger = logging.getLogger("root")
#logging.basicConfig(
    #format = "\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    #level=logging.DEBUG
#)

logger = logging.getLogger("accountability_tracker")

# Create your views here.
@xframe_options_sameorigin
def index(request):
    contributions = InitiativeContributor.objects.all()

    supporting_contributions = contributions.filter(stance="Support")
    opposing_contributions = contributions.filter(stance="Oppose")



    total_sum = contributions.values("initiative_identifier").annotate(total=Sum("amount"))
    supporting_sum = supporting_contributions.values("initiative_identifier").annotate(total=Sum("amount"))
    opposing_sum = opposing_contributions.values("initiative_identifier").annotate(total=Sum("amount"))

    return render_to_response("index.html", {
        "total_sum": total_sum,
        "supporting_sum": supporting_sum,
        "opposing_sum": opposing_sum
    })


#class DummyListView(View):
    """
    Generates a page that will feature a list linking to detail pages about
    each object in the queryset.
    """

    #queryset = InitiativeContributor.objects.values("initiative_identifier").annotate(total=Sum("amount"))
    #template_name = "index.html"

    #def display(self, request):
        #return render(request, self.template_name, {
            #"data": queryset
        #})
