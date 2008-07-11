from django.http import HttpResponse
from django.template import Template
from django.shortcuts import render_to_response

def index(request):
  """index for join section"""
  return render_to_response('join_index.html', {})