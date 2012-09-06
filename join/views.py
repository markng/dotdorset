from django.http import HttpResponse
from django.template import Template
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
  """index for join section"""
  return render_to_response('join_index.html', RequestContext(request))