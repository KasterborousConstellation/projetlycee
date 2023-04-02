import hashlib
from .models import Student
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