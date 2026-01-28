from django.contrib import admin, messages
from django.db.models.functions import Length
from django.utils.safestring import mark_safe

from .models import Student, Category



class ManualFilter(admin.SimpleListFilter):
    title = "Manual availability"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("manual is present", "manual+"),
            ("no manual", "manual-"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "manual is present":
            return queryset.filter(manual__isnull=False)
        elif self.value() == "no manual":
            return queryset.filter(manual__isnull=True)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('post_photo',)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "post_photo", "time_create", "is_published", "cat")
    list_display_links = ("title",)
    ordering = ("time_create", "title")
    list_editable = ("is_published", "cat")
    list_per_page = 10
    actions = ("set_published", "set_draft")
    search_fields = ("title",)
    list_filter = (ManualFilter, "cat__name", "is_published")
    save_on_top = True

    @admin.display(description="Photo", ordering=Length("content"))
    def post_photo(self, student: Student):
        if student.photo:
            return mark_safe(f"<img src='{student.photo.url}' width=50>")
        return "No Photo"

    @admin.action(description="Publishing posts")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Student.PostStatus.PUBLISHED)
        self.message_user(request, f"{count} posts published")

    @admin.action(description="Deactivating posts")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Student.PostStatus.DRAFT)
        self.message_user(request, f"{count} posts moved to draft", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_display_links = ("id", "name", )