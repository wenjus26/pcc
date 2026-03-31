from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('citizens/', include('apps.citizens.urls')),
    path('institutions/', include('apps.institutions.urls')),
    path('matching/', include('apps.matching.urls')),
    path('content/', include('apps.content.urls')),
    path('evaluations/', include('apps.evaluations.urls')),
    path('community/', include('apps.community.urls')),
)

handler400 = 'apps.core.views.error_400'
handler403 = 'apps.core.views.error_403'
handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

