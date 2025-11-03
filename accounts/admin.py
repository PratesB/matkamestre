from django.contrib import admin
from .models import CustomUser, MentorProfile, MenteeProfile, InvitationToken
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_mentor', 'mentor', 'created_at', 'updated_at']




@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'language', 'get_bio_summary', 'get_profile_picture')
    search_fields = ('user__email', 'professional_career', 'language')
    list_filter = ('language',)

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('bio', 'professional_career', 'language')
        }),
        ('Profile Media', {
            'fields': ('profile_picture',)
        }),
    )
    

    @admin.display(description='Mentor Email', empty_value='-')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description='Bio Summary')
    def get_bio_summary(self, obj):
        return (obj.bio[:75] + '...') if obj.bio and len(obj.bio) > 75 else obj.bio
    
    @admin.display(description='Profile Picture')
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return '-'




@admin.register(MenteeProfile)
class MenteeProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'location', 'language', 'created_at', 'get_profile_picture')
    search_fields = ('user__email', 'location', 'professional_career', 'professional_goal')
    list_filter = ('location',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'profile_picture')
        }),
        ('Professional Information', {
            'fields': ('professional_career', 'professional_goal', 'location', 'language', 'cv_file')
        }),
        ('Mentor Feedback', {
            'classes': ('collapse',),
            'fields': ('cv_analysis_feedback',) # This will now render as a file upload field
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


    @admin.display(description='Mentee Email', empty_value='-')
    def user_email(self, obj):
        return obj.user.email
    

    @admin.display(description='Profile Picture')
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return '-'





@admin.register(InvitationToken)
class InvitationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'mentee_email', 'mentor_email', 'expires_at', 'is_used', 'created_at')


    @admin.display(description='Inviting Mentor Email', empty_value='-')
    def mentor_email(self, obj):
        return obj.mentor.email
   
