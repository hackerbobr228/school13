from django.contrib import admin
from django.utils.html import format_html
from .models import SchoolClass, Student, Nomination, StudentNomination, SchoolSettings

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'class_teacher', 'student_count', 'created_at']
    list_filter = ['grade', 'section']
    search_fields = ['class_teacher']
    ordering = ['grade', 'section']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('grade', 'section', 'class_teacher')
        }),
        ('Дополнительная информация', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'school_class', 'age', 'gender', 'photo_preview', 'is_active']
    list_filter = ['school_class__grade', 'school_class__section', 'gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'student_id', 'parent_name']
    ordering = ['school_class__grade', 'school_class__section', 'last_name']
    list_per_page = 50
    
    fieldsets = (
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'photo', 'birth_date', 'gender')
        }),
        ('Школьная информация', {
            'fields': ('school_class','is_active')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email', 'address'),
            'classes': ('collapse',)
        }),
        ('Информация о родителях', {
            'fields': ('parent_name', 'parent_phone'),
            'classes': ('collapse',)
        }),
        ('Дополнительная информация', {
            'fields': ('achievements', 'hobbies'),
            'classes': ('collapse',)
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = "Фото"

@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'name', 'is_active', 'recipients_count']
    list_filter = ['is_active', 'name']
    search_fields = ['title_ru', 'title_uz']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'image', 'is_active')
        }),
        ('Русский язык', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Узбекский язык', {
            'fields': ('title_uz', 'description_uz')
        }),
    )
    
    def recipients_count(self, obj):
        return obj.recipients.count()
    recipients_count.short_description = "Получателей"

@admin.register(StudentNomination)
class StudentNominationAdmin(admin.ModelAdmin):
    list_display = ['student', 'nomination', 'date_awarded', 'score']
    list_filter = ['nomination', 'date_awarded', 'student__school_class']
    search_fields = ['student__first_name', 'student__last_name', 'achievement_description']
    date_hierarchy = 'date_awarded'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('student', 'nomination', 'date_awarded') 
        }),
        ('Детали достижения', {
            'fields': ('score', )
        }),
    )


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основная информация', {
            'fields': ('school_name_ru', 'school_name_uz', 'total_students', 'total_achievements')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'telegram', 'address_ru', 'address_uz')
        }),
        ('О школе', {
            'fields': ('about_ru', 'about_uz'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return not SchoolSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

# Customize admin interface
admin.site.site_header = "Школа №13 - Панель Администратора"
admin.site.site_title = "Школа №13"
admin.site.index_title = "Управление сайтом школы"
