from django.db import models

class Place(models.Model):
    name=models.CharField(max_length=140); category=models.CharField(max_length=40); description=models.TextField()
    area=models.CharField(max_length=100); lat=models.FloatField(); lng=models.FloatField(); price=models.PositiveIntegerField(default=0)
    duration=models.PositiveIntegerField(default=60); hours=models.CharField(max_length=100,default='09:00-18:00')
    verified=models.BooleanField(default=True); source=models.CharField(max_length=160,default='RoamWise destination partner directory')
    checked=models.CharField(max_length=30,default='2026-10-15'); access=models.CharField(max_length=180,blank=True)
    tags=models.JSONField(default=list); booking_url=models.URLField(blank=True); carbon=models.FloatField(default=.7)

class Trip(models.Model):
    title=models.CharField(max_length=180); destination=models.CharField(max_length=100,default='Jaipur, India')
    days=models.PositiveIntegerField(default=2); budget=models.PositiveIntegerField(default=5000); party=models.PositiveIntegerField(default=1)
    preferences=models.JSONField(default=dict); plan=models.JSONField(default=list); share_code=models.CharField(max_length=12,unique=True)
    created=models.DateTimeField(auto_now_add=True)

class Expense(models.Model):
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='expenses'); title=models.CharField(max_length=120)
    amount=models.FloatField(); payer=models.CharField(max_length=80); currency=models.CharField(max_length=5,default='INR')

class Vote(models.Model):
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='votes'); place_id=models.PositiveIntegerField()
    voter=models.CharField(max_length=80); created=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=[('trip','place_id','voter')]

class BusinessSubmission(models.Model):
    name=models.CharField(max_length=160); category=models.CharField(max_length=50); area=models.CharField(max_length=120)
    contact=models.CharField(max_length=160); description=models.TextField(); status=models.CharField(max_length=20,default='Pending review')
    created=models.DateTimeField(auto_now_add=True)

class ListingReport(models.Model):
    place_id=models.PositiveIntegerField(); reason=models.CharField(max_length=80); details=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
