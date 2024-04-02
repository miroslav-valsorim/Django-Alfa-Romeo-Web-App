from django.contrib import admin

from alfa_romeo_web.forum.models import ForumCategory, Post, Comment


@admin.register(ForumCategory)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    list_per_page = 20
    ordering = ('pk',)


@admin.register(Post)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'user', 'approved', 'closed', 'get_categories',)
    list_per_page = 20
    ordering = ('pk', )
    search_fields = ('title',)
    search_help_text = 'Search by Post Title'
    list_filter = ('approved', 'closed',)

    def get_categories(self, obj):
        return ", ".join([category.title for category in obj.categories.all()])

    get_categories.short_description = 'Categories'


@admin.register(Comment)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'content', 'date',)
    list_per_page = 20
    ordering = ('date', 'pk',)
    search_fields = ('user',)
    search_help_text = 'Search by User'


