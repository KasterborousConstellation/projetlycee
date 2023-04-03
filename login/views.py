from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from .utility import sha256, has_student, get_student, createUUID
from .models import Token
import datetime
@csrf_protect
def loginPage(request):
    template = loader.get_template('login/index.html')
    return HttpResponse(template.render(request=request))
def error(request):
    template = loader.get_template('login/error.html')
    return HttpResponse(template.render(request=request))

def login(request):
    if(request.method =='POST'):
        post = request.POST
        id = post["id"]
        #Encode le mot de passe en sha256.
        password = f"{post['password']}".encode()
        password = sha256(password)
        #Verifie si l'élève existe
        if(has_student(id)):
            student = get_student(id)
            #Verification que l'élève a entrer le bon mot de passe
            if(password==student.password):
                #TODO Create token
                token = Token(UUID=createUUID(), student=student)
                token.save()
                return redirect(f"/soutien/?identifiant={ token.UUID }")
            else: 
                return redirect(loginPage)
        else:
            print("no student with that id")
            return redirect(loginPage)
    else:
        return redirect(error)
    
def site(request):
    query = request.GET.get('identifiant',None)
    #Recherche des tokens avec cet identifiant (Normalement y'en a qu'un)
    a = Token.objects.filter(UUID=query)
    #Validation du Token 
    #TODO Expiration des Tokens
    if(len(a)==0):
        return redirect(loginPage)
    student = a[0].student
    distance = ((datetime.datetime.now(datetime.timezone.utc)-a[0].creation_date))
    print(distance)
    return render(request,'login/login.html',{"nom":student.nom,"prenom":student.prenom,"serie":student.serie})