# django imports
from django.contrib import admin

# inner modules imports
from .models import PageData, Footer


# Register your models here.
@admin.register(PageData)
class PageDataAdmin(admin.ModelAdmin):
    readonly_fields = [
        "banner_preview",
    ]
    list_display = ("name", "title", "target_name", "banner_preview")
    search_fields = ("name", "title", "targer_name")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "target_name",
                    "title",
                    ("banner", "banner_preview"),
                    "route",
                    "footer",
                )
            },
        ),
    )


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    readonly_fields = ["logo_preview"]
    list_display = ("footer_name", "footer_phone", "footer_email", "logo_preview")
    search_fields = ("footer_name", "footer_phone", "footer_email")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "footer_name",
                    "footer_phone",
                    ("footer_logo", "logo_preview"),
                    "footer_email",
                    "footer_text",
                )
            },
        ),
        (
            "Social Links",
            {
                "classes": ("collapse", "close"),
                "fields": (
                    "footer_youtube",
                    "footer_telegram",
                    "footer_instagram",
                    "footer_googleplus",
                    "footer_twitter",
                ),
            },
        ),
    )
