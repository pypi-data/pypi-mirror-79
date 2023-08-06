from django.contrib.admin import ModelAdmin


class ArticleBookmarkModelSchemeAdmin(ModelAdmin):
    list_display   = ["user", "article", "created_at"]
    list_filter    = ["created_at", "updated_at"]
    search_fields  = ["user", "article"]
    list_per_page  = 10
    fieldsets      = (
        ("Bookmark data", {
            "classes": ["extrapretty"],
            "fields": ["article", "user"]
        }),
    )