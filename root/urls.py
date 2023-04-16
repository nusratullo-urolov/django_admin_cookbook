from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from root import settings

#admin paneldagi pagening eng tepasida chiqib turadi
admin.site.site_header = "Nusratullo"

# saytni urldan ham tepada turadi ya'ni vkladka chiqadigan text
admin.site.site_title = "Nusratullo Admin"

# site_headerdan pastroqda chiqib turadi
admin.site.index_title = "Nusratullo Urolov"

urlpatterns = [
    path('admin/', admin.site.urls),
    # ikkinchi admin sayt uchun url
    # path('event-admin/', event_admin_site.urls),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) +  static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
