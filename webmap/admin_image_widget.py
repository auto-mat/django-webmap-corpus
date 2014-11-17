# originated from https://djangosnippets.org/snippets/2455/

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from PIL import Image
import os

try:
    from easy_thumbnails.files import get_thumbnailer

    def thumbnail(image_path):
        thumbnailer = get_thumbnailer(image_path)
        thumbnail_options = {'crop': False, 'size': (160, 160), 'detail': True, 'upscale': False}
        t = thumbnailer.get_thumbnail(thumbnail_options)
        media_url = settings.MEDIA_URL
        return u'<img src="%s%s" alt="%s"/>' % (media_url, t, image_path)
except ImportError:
    def thumbnail(image_path):
        absolute_url = os.path.join(settings.MEDIA_URL, image_path)
        return u'<img src="%s" alt="%s" />' % (absolute_url, image_path)


def list_display(image):
    file_name = str(image)
    if file_name:
        file_path = '%s%s' % (settings.MEDIA_URL, file_name)
        try:            # is image
            Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
            return '<a target="_blank" href="%s">%s</a>' % (file_path, thumbnail(file_name),)
        except IOError:  # not image
            return None


class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append('<a target="_blank" href="%s">%s</a>' %
                    (file_path, thumbnail(file_name),))
            except IOError:  # not image
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' %
                    (_('Currently:'), file_path, file_name, _('Change:')))

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
