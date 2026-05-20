from django.db import models
from django.contrib.auth.models import User

SKILL_CHOICES = [
    ('Frontend', 'Frontend'),
    ('Backend', 'Backend'),
    ('Design', 'Design'),
    ('DevOps', 'DevOps'),
    ('Other', 'Other'),
]

PLATFORM_CHOICES = [
    ('LinkedIn', 'LinkedIn'),
    ('Twitter / X', 'Twitter / X'),
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook'),
    ('TikTok', 'TikTok'),
]

INDUSTRY_CHOICES = [
    ('Startup', 'Startup'),
    ('Agenție', 'Agenție'),
    ('Corporație', 'Corporație'),
    ('ONG', 'ONG'),
    ('Persoană fizică', 'Persoană fizică'),
    ('Altele', 'Altele'),
]


class Freelancer(models.Model):
    """Programatorul / designerul / devops-ul care oferă servicii."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, blank=True, related_name='freelancer_profile'
    )
    full_name = models.CharField(max_length=200)
    skill = models.CharField(max_length=100, choices=SKILL_CHOICES)
    description = models.TextField(blank=True, default='')
    experience_years = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.full_name} ({self.skill})"


class ClientProfile(models.Model):
    """Firma sau persoana care caută freelanceri."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, blank=True, related_name='client_profile'
    )
    full_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True, default='')
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.full_name}" + (f" ({self.company})" if self.company else '')


class Lead(models.Model):
    """
    Mesaj trimis de un client către un freelancer.
    'Lead' e termenul de marketing — în UI apare ca 'Contact' sau 'Mesaj'.
    """
    client = models.ForeignKey(
        ClientProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sent_messages'
    )
    freelancer = models.ForeignKey(
        Freelancer, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='received_messages'
    )
    # Câmpuri fallback dacă trimite cineva nelogat
    sender_name = models.CharField(max_length=200, blank=True)
    sender_email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_sender_name(self):
        return self.client.full_name if self.client else self.sender_name

    def get_sender_email(self):
        return self.client.user.email if self.client and self.client.user else self.sender_email

    def __str__(self):
        return f"{self.get_sender_name()} → {self.freelancer} ({self.created_at:%d %b %Y})"


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    excerpt = models.TextField()
    body = models.TextField()
    category = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Campaign(models.Model):
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    PLATFORM_ICONS = {
        'LinkedIn': '💼', 'Twitter / X': '🐦',
        'Instagram': '📸', 'Facebook': '📘', 'TikTok': '🎵',
    }

    @property
    def icon(self):
        return self.PLATFORM_ICONS.get(self.platform, '📣')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.platform}: {self.text[:50]}"
