from django.contrib import admin
from .models import Category, Skill, CitizenProfile, Experience, Education, Document

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1

@admin.register(CitizenProfile)
class CitizenProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_title', 'location', 'is_public', 'is_validated', 'charter_signed')
    list_filter = ('is_public', 'is_validated', 'location', 'charter_signed')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'current_title')
    inlines = [ExperienceInline, EducationInline, DocumentInline]
    filter_horizontal = ('skills',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'position', 'start_date', 'is_current')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'institution', 'degree', 'field_of_study')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'doc_type', 'is_verified', 'uploaded_at')
    list_filter = ('doc_type', 'is_verified')
