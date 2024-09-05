from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from maykin_2fa import monkeypatch_admin
from maykin_2fa.urls import urlpatterns, webauthn_urlpatterns

from woo_publications.accounts.views.password_reset import PasswordResetView

# Configure admin

monkeypatch_admin()

handler500 = "woo_publications.utils.views.server_error"
admin.site.site_header = _("WOO publications")
admin.site.site_title = _("WOO publications")
admin.site.index_title = _("WOO publications dashboard")

# URL routing

urlpatterns = [
    path(
        "admin/password_reset/",
        PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    # Use custom login views for the admin + support hardware tokens
    path("admin/", include((urlpatterns, "maykin_2fa"))),
    path("admin/", include((webauthn_urlpatterns, "two_factor"))),
    path("admin/hijack/", include("hijack.urls")),
    path("admin/", admin.site.urls),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Simply show the index template.
    path("", TemplateView.as_view(template_name="master.html"), name="root"),
]

# NOTE: The staticfiles_urlpatterns also discovers static files (ie. no need to run collectstatic). Both the static
# folder and the media folder are only served via Django if DEBUG = True.
urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG and apps.is_installed("debug_toolbar"):
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

if apps.is_installed("rosetta"):  # pragma: no cover
    urlpatterns = [path("admin/rosetta/", include("rosetta.urls"))] + urlpatterns
