from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email=models.EmailField(max_length=254, unique=True)
    is_mentor = models.BooleanField(default=False)
    mentor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'Email: {self.email} | Is Mentor: {self.is_mentor} | Created at: {self.created_at}'




class MentorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(blank=True, null=True)
    professional_career = models.TextField(
        blank=True,
        null=True,
        verbose_name="Professional Background",
    )
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fi', 'Finnish'),
        ('sv', 'Swedish'),
        ('es', 'Spanish (Español)'),
        ('pt', 'Portuguese (Português)'),
        ('zh', 'Chinese (Mandarim)'),
        ('hi', 'Hindi'),
        ('ar', 'Arabic (العربية)'),
        ('fr', 'French (Français)'),
        ('ru', 'Russian (Русский)'),
        ('de', 'German (Deutsch)'),
        ('it', 'Italian (Italiano)'),
        ('ja', 'Japanese (日本語)'),
        ('ko', 'Korean (한국어)'),
        ('nl', 'Dutch (Nederlands)'),
        ('tr', 'Turkish (Türkçe)'),
        ('pl', 'Polish (Polski)'),
        ('cs', 'Czech (Čeština)'),
        ('uk', 'Ukrainian (Українська)'),
        ('fa', 'Farsi (Persian/Dari)'),
        ('so', 'Somali'),
    ]
    language = models.TextField(
        blank=True,
        null=True,
        help_text="Languages spoken for mentoring."
    )
    profile_picture = models.ImageField(upload_to='profiles/mentor/', null=True, blank=True)

    def __str__(self):
        return f'Mentor profile of {self.user.email}'
    


class MenteeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentee_profile')
    
    # --- New Field 1: CV/Resume (PDF File) ---
    cv_file = models.FileField(
        upload_to='mentee_files/cv/', 
        null=True, 
        blank=True,
        verbose_name="CV/Resume (PDF)"
    )

    # --- New Field 2: Language Proficiency ---
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fi', 'Finnish'),
        ('sv', 'Swedish'),
        ('es', 'Spanish (Español)'),
        ('pt', 'Portuguese (Português)'),
        ('zh', 'Chinese (Mandarim)'),
        ('hi', 'Hindi'),
        ('ar', 'Arabic (العربية)'),
        ('fr', 'French (Français)'),
        ('ru', 'Russian (Русский)'),
        ('de', 'German (Deutsch)'),
        ('it', 'Italian (Italiano)'),
        ('ja', 'Japanese (日本語)'),
        ('ko', 'Korean (한국어)'),
        ('nl', 'Dutch (Nederlands)'),
        ('tr', 'Turkish (Türkçe)'),
        ('pl', 'Polish (Polski)'),
        ('cs', 'Czech (Čeština)'),
        ('uk', 'Ukrainian (Українська)'),
        ('fa', 'Farsi (Persian/Dari)'),
        ('tr', 'Turkish (Türkçe)'),
        ('so', 'Somali')
    ]
    # Note: Use a comma-separated string or a separate many-to-many field for multiple languages/levels
    language = models.TextField(
        blank=True,
        null=True,
        help_text="Primary language for coaching/job search."
    )

    # --- New Field 3: Location ---
    # Stores the preferred working city/region in Finland
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Preferred working location (e.g., Helsinki, Tampere, Remote)."
    )

    # --- New Field 4: Professional Career (Description/Goals) ---
    # Used for AI matching and mentor briefing
    professional_career = models.TextField(
        blank=True,
        null=True,
        verbose_name="Professional Background",
    )

    # --- New Field: Professional Goal ---
    professional_goal = models.TextField(
        blank=True,
        null=True,
        verbose_name="Professional Goal",
        help_text="Describe your professional goals in Finland."
    )

    # --- New Field 5: CV Analysis Feedback (PDF) ---
    # Can be populated by a mentor or an AI tool
    cv_analysis_feedback = models.FileField(
        upload_to='mentee_files/cv_analysis/',
        blank=True,
        null=True,
        verbose_name="CV Analysis Feedback (PDF)",
        help_text="Initial feedback on the mentee's CV, uploaded as a PDF."
    )
    
    profile_picture = models.ImageField(upload_to='profiles/mentee/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Mentee profile: {self.user.email}'
    



class InvitationToken(models.Model):
    token = models.CharField(max_length=100, unique=True)
    mentee_email = models.EmailField(max_length=254)
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'Token for {self.mentee_email} by {self.mentor.email}'