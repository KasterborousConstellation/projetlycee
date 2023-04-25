from django.db import models

# Create your models here.
class Student(models.Model):
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=30)
    autorisation = models.IntegerField(null=True)
    serie = models.CharField(max_length=3,default="gen")
    classe = models.IntegerField(default=1)
    identifiant = models.CharField(max_length=128,default='eleve')
    password = models.CharField(max_length=64,default="")
    genre = models.CharField(max_length=1,default="M")
    
class Token(models.Model):
    UUID = models.CharField(max_length=20,unique=True)
    creation_date= models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)

class Room(models.Model):
    name = models.CharField(max_length=30,unique=True)

class Slot(models.Model):
    matiere= models.CharField(max_length=20)
    heure = models.IntegerField()
    room = models.ForeignKey(Room,on_delete=models.CASCADE,null=True)

class Class(models.Model):
    professor = models.ForeignKey(Student,on_delete=models.CASCADE)
    targeted_level = models.IntegerField(default=0)
    places = models.IntegerField(default=5)
    students = models.ManyToManyField(Student,related_name="class_student")
    month = models.IntegerField(default=1)
    day = models.IntegerField(default=1)
    slot = models.ForeignKey(Slot,on_delete=models.CASCADE,default=None,null=True)

#To run python manage.py migrate --fake login zero