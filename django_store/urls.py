from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Add this for language switching
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('checkout/', include('checkout.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', include('store.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
