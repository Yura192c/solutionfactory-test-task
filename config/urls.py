from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', include('routers')),
    path('account/', include('src.user.urls')),
    path('ui/', include(('src.stats.urls', 'stats'), namespace='stats')),
]
