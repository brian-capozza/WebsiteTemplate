import os
import logging

from PIL import Image

from django.conf import settings
from django import template

logger = logging.getLogger(__name__)
register = template.Library()


def convert_to_webp(image_path):
    webp_image_path = image_path.rsplit('.', 1)[0] + '.webp'

    if not os.path.exists(webp_image_path):
        try:
            img = Image.open(image_path)

            img.save(webp_image_path, 'WEBP')
            logger.debug(f'Converted {image_path} to WEBP')
        except Exception as e:
            logger.debug(f'Could not convert {image_path} to WEBP. Error: {e}')



@register.simple_tag(takes_context=True)
def webp(context, img_url):
    static_path = settings.STATIC_URL + img_url

    try:
        request = context['request']

        if 'image/webp' in request.META.get('HTTP_ACCEPT', ''):
            webp_static_path = settings.STATIC_URL + img_url.rsplit('.', 1)[0] + '.webp'

            webp_file_path = os.path.join(settings.BASE_DIR, 'static', img_url.rsplit('.', 1)[0] + '.webp')
            if os.path.exists(webp_file_path):
                return webp_static_path
            else:
                convert_to_webp(os.path.join(settings.BASE_DIR, 'static', img_url))
                return webp_static_path
            
        return static_path
    except KeyError:
        return static_path