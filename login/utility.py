import hashlib
from .models import Student
from random import randint
def sha256(mdp):
    m = hashlib.sha256()
    m.update(mdp)
    return m.hexdigest()
def has_student(identifiant):
    query = Student.objects.all()
    for student in query:
        if(student.identifiant.upper()==identifiant.upper()):
            return True
    return False
def get_student(id):
    query = Student.objects.filter(identifiant=id)
    return query[0]
def createUUID():
    data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ0123456789"
    char = ''
    for i in range(20):
        char = char + data[randint(0,len(data)-1)]
    return char