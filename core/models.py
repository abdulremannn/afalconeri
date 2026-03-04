from django.db import models
import json


class DroneSystem(models.Model):
    STATUS_CHOICES = [
        ('OPERATIONAL', 'Operational'),
        ('DEVELOPMENT', 'Development'),
        ('PROTOTYPE', 'Prototype'),
    ]
    order       = models.IntegerField(default=0)
    system_id   = models.CharField(max_length=50, unique=True)
    name        = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    system_class= models.CharField(max_length=100)
    tagline     = models.CharField(max_length=200)
    description = models.TextField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPERATIONAL')
    image       = models.ImageField(upload_to='systems/', blank=True, null=True)
    specs_json  = models.TextField(default='[]')
    features_json = models.TextField(default='[]')
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def get_specs(self):
        try: return json.loads(self.specs_json)
        except: return []

    def get_features(self):
        try: return json.loads(self.features_json)
        except: return []

    def __str__(self): return self.name


class Capability(models.Model):
    order       = models.IntegerField(default=0)
    cap_id      = models.CharField(max_length=50, unique=True)
    number      = models.CharField(max_length=5)
    title       = models.CharField(max_length=100)
    subtitle    = models.CharField(max_length=200)
    description = models.TextField()
    items_json  = models.TextField(default='[]')  # JSON list of strings
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def get_items(self):
        try: return json.loads(self.items_json)
        except: return []

    def __str__(self): return self.title


class ContactInfo(models.Model):
    headquarters  = models.CharField(max_length=200, default='')
    postal        = models.CharField(max_length=200, default='')
    secure_comms  = models.CharField(max_length=200, default='')
    inquiries_email = models.CharField(max_length=200, default='')
    disclaimer    = models.TextField(default='')
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Contact Info'

    def __str__(self): return 'Contact Information'


class AdminUser(models.Model):
    username      = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=256)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self): return self.username
