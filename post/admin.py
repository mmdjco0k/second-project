from django.contrib import admin
from .models import PostModel , RecyclePost

@admin.register(PostModel)
class PostModel(admin.ModelAdmin):
    pass


@admin.register(RecyclePost)
class RecycleArticlesAdmin(admin.ModelAdmin):
    actions = ["recover"]

    def get_queryset(self, request):
        return RecyclePost.objects.filter(is_deleted=True)

    def recover(self, request, queryset):
        queryset.update(is_deleted=False, status=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions