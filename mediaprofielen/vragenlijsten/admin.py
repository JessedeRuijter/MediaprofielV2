from django.contrib import admin
from vragenlijsten.models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from django.core.management import call_command
from django.contrib import admin
from ajax_select import make_ajax_form
from utils import addScore
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class ChoiceInline(NestedTabularInline):
    model = QuestionChoice
    extra = 0
    fk_name = 'question'

class QuestionInline(NestedTabularInline):
    model = Question
    extra = 0
    fk_name = 'block'
    inlines = [ChoiceInline]

class QuestionBlockInline(NestedStackedInline):
    model = QuestionBlock
    extra = 0
    fk_name = 'enquete'
    inlines = [QuestionInline]

class EnqueteAdmin(NestedModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Description',      {'fields': ['description']}),
        ('Date information', {'fields': ['publishedDate']}),        
        ('Locked', {'fields': ['locked']})
    ]
    inlines = [QuestionBlockInline]

# @admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields= ('members',)
    form = make_ajax_form(Organisation, {
        # fieldname: channel_name
        'owners': 'users'
    })
    # actions = ['fix_profiles']
    # def fix_profiles(self, request, queryset):
    #     for org in queryset:
    #         for member in org.members.all():
    #             addScore(member, 24, 92)

class CustomUserAdmin(BaseUserAdmin):
    actions = ['fix_profile']
    def fix_profile(self, request, queryset):
        for user in queryset:
            addScore(user, 24, 92)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Enquete, EnqueteAdmin)
admin.site.register(Profiel)
admin.site.register(Invulmoment)
admin.site.register(Account)
admin.site.register(Answer)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(ProfileText)
