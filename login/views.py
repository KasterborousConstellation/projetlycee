from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from .utility import sha256, has_student, get_student, createUUID, convert_serie,get_classe,getNextWeek,getMonth,getFinalDayForInscription,get_matiere,get_style_attribute
from .models import Token,Student,Class
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
@csrf_protect
def site(request):
    query = request.GET.get('identifiant',None)
    search = request.GET.get('query',None)
    if(search == None or search=="" or len(search)==0):
        search=None
    #Recherche des tokens avec cet identifiant (Normalement y'en a qu'un)
    a = Token.objects.filter(UUID=query)
    len_of_a = a.count
    #Validation du Token 
    #TODO Expiration des Tokens
    if(len_of_a==0):
        return redirect(loginPage)
    token = a[0]
    student = token.student
    time_since_token = ((datetime.datetime.now(datetime.timezone.utc)-token.creation_date))/ datetime.timedelta(seconds=1)
    #Vérifie la validité du Token.
    if(time_since_token<30* 60):
        #Crée l'URL de la page
        url = ""
        uri = str(request.build_absolute_uri())
        index =0
        char =""
        while char!="?":
            char=uri[index]
            url+=char
            index+=1
        url+="identifiant="+token.UUID+"&query="
        #Recupère toute les matières et génère les urls de trie par matière
        cours = get_matiere()
        url_cours = [(elt[0],url+elt[0]) for elt in cours]
        url_cours.append(("Tous",url))
        #Génère les jours de la semaine et les heures
        jours = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi"]
        jours_id = getNextWeek()
        formatted_day = [ (jours[i]+" "+str(jours_id[i][0])+" "+str(getMonth(jours_id[i][1]))) for i in range(5)  ]
        hours =["8:05","9:00","10:10","11:05","12:00","13:00","13:55","14:50","16:00","16:55","17:50"]
        #Génère le contexte de variable pour la template
        context ={}
        context["id"]=token.UUID
        context["nom"]=student.nom
        context["prenom"]=student.prenom
        context["serie"]=convert_serie(student.serie)
        context["urls"]=url_cours
        context["path"]="/soutien/?identifiant="+token.UUID+"&query="
        context["hours"]=hours
        context["days"]=formatted_day
        context["classe"]=get_classe(student.classe)
        context["n5"]=range(5)
        context["autorisation"]= student.autorisation
        classes = Class.objects.all()
        array = {}
        for hour in hours:
            crenaux_p_heure = []
            crenaux_p_heure_addon =[]
            for jours in jours_id:
                classe = classes.filter(day=jours[0],month=jours[1])
                if(len(classe)==0):
                    crenaux_p_heure.append(None)
                    crenaux_p_heure_addon.append(None)
                else:
                    current_classe = classe[0]
                    if(search!=None):
                        if(search.upper()!=current_classe.slot.matiere.upper()):
                            crenaux_p_heure.append(None)
                            crenaux_p_heure_addon.append(None)
                            continue
                    if(hours[current_classe.slot.heure]==hour):
                        crenaux_p_heure.append([current_classe.slot.matiere,current_classe.professor.nom,get_style_attribute(current_classe.slot.matiere),current_classe.professor.genre])
                        is_present = len(current_classe.students.all().filter(id=student.id))>0
                        crenaux_p_heure_addon.append([current_classe.places-len(current_classe.students.all()),current_classe.places,is_present,current_classe.id,get_style_attribute(current_classe.slot.matiere)])
                    else:
                        crenaux_p_heure.append(None)
                        crenaux_p_heure_addon.append(None)
                array[hour]=[hour,crenaux_p_heure,crenaux_p_heure_addon]
        context["crenaux"]= array
        context["first_day"]=formatted_day[0]
        context["last_day"]=formatted_day[-1]
        final_day = getFinalDayForInscription()
        context["final_day"]= "Vendredi "+str(final_day[0])+" "+getMonth(final_day[1])
        return render(request,'login/login.html',context)
    else:
        return redirect(loginPage)
    
def subscribe(request):
    #Regénère l'url de départ
    parameters="identifiant="+request.POST.get("id")
    url = f'/{"soutien/"}?{parameters}'
    #Recupère l'id de la classe ou l'on veut s'inscrire 'subscribe' ainsi que le token de connexion
    class_id= request.POST.get('subscribe')
    token = request.POST.get('id')
    student = Token.objects.all().filter(UUID=token)[0].student
    current_class = Class.objects.all().filter(id=class_id)[0]
    has_student = len(current_class.students.all().filter(id=student.id))>0
    #Vérifie si il reste encore des places
    if(current_class.places>len(current_class.students.all())):
        #Ajoute ou retire l'eleve aux élèves inscrits.
        if(has_student):
            current_class.students.remove(student)
        else:
            current_class.students.add(student)
    #Redirection à l'url de départ
    return redirect(url)