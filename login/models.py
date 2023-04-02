from django.db import models

# Create your models here.
class Student(models.Model):
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=30)
    autorisation = models.IntegerField(null=True)
    serie = models.CharField(max_length=3,default="gen")
    identifiant = models.CharField(max_length=20,default='eleve')
    password = models.CharField(max_length=64,default="")
class Token(models.Model):
    UUID = models.CharField(max_length=20,unique=True)
    creation_date= models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)