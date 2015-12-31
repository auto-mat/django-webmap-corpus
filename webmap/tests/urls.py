"""URLs to run the tests."""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = (
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webmap/', include('webmap.urls')),
)


if settings.DEBUG:
    urlpatterns += (
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
