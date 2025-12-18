from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class EEGFile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('error', 'Erro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='eeg_files/')
    original_name = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField()
    # Adicionamos este campo para o dashboard funcionar
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

class Analysis(models.Model):
    eeg_file = models.OneToOneField(EEGFile, on_delete=models.CASCADE)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    classification = models.BooleanField(default=False) # True = TEA, False = Não TEA
    confidence = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Analysis of {self.eeg_file.original_name}"

class ReportConfig(models.Model):
    FREQUENCY_CHOICES = [
        ('on_demand', 'Sob demanda'),
        ('daily', 'Diária'),
        ('weekly', 'Semanal'),
    ]
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('html', 'HTML'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='on_demand')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

# Sinais
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()