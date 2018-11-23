"""
For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/views/
"""
from django.http import HttpResponse, HttpResponseBadRequest
from django import forms
from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.http import etag
from django.urls import reverse
from PIL import Image, ImageDraw
from io import BytesIO
import hashlib


class ImageForm(forms.Form):
    width = forms.IntegerField(min_value=1, max_value=1000)
    height = forms.IntegerField(min_value=1, max_value=1000)


def home(request):
    example_url = reverse('get_placeholder_image', kwargs={'width': 80, 'height': 50})
    example_url = request.build_absolute_uri(example_url)
    context = {
        'example_url': example_url,
    }
    return render(request, 'home.html', context)


def create_placeholder_image(height, width, format='PNG'):
    key = '{}.{}.{}'.format(width, height, format)
    buffer = cache.get(key)
    print(buffer)
    if buffer is None:
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        text = '{} X {}'.format(height, width)
        text_width, text_height = draw.textsize(text)
        if text_width < width and text_height < height:
            text_top = (height - text_height) // 2
            text_left = (width - text_width) // 2
            draw.text((text_left, text_top), text, fill=(255, 255, 255))
        buffer = BytesIO()
        image.save(buffer, format)
        buffer.seek(0)
        cache.set(key, buffer, 60 * 60)
    return buffer


def genernate_etag(request, height, width):
    content = 'placeholder.{}.{}'.format(height, width)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(genernate_etag)
def get_placeholder_image(request, height, width):
    form = ImageForm({'width': width, 'height': height})
    if form.is_valid():
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        image = create_placeholder_image(height, width)
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('FAIL')

