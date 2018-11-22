"""
For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/views/
"""
from django.http import HttpResponse
import datetime


def helloworld_page(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
