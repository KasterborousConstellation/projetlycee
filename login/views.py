from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from .utility import sha256, has_student, get_student, createUUID, convert_serie,get_classe,getNextWeek,getMonth,getFinalDayForInscription,get_matiere,get_style_attribute,convert_hour,format_next_monday,convert_day_to_int,convert_hour_to_int,convert_niveau_to_int,subselect,onlyvalid
from .models import Token,Student,Class,Slot,Room
from .connection import connect
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
    search = request.GET.get('query',None)
    if(search == None or search=="" or len(search)==0):
        search=None
    connection = connect(request)
    #Vérifie la validité du Token.
    if(connection.is_valid()):
        student = connection.student
        token = connection.token
        #Crée l'URL de la page
        url = ""
        uri = str(request.build_absolute_uri())
        index =0
        char =""
        while char!="?":
            char=uri[index]
            url+=char
            index+=1
        contructed_url=url+"identifiant="+token.UUID+"&query="
        #Recupère toute les matières et génère les urls de trie par matière
        cours = get_matiere()
        url_cours = [(elt[0],contructed_url+elt[0]) for elt in cours]
        url_cours.append(("Tous",contructed_url))
        #Génère les jours de la semaine et les heures
        jours = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi"]
        jours_id = getNextWeek()
        formatted_day = [ (jours[i]+" "+str(jours_id[i][0])+" "+str(getMonth(jours_id[i][1]))) for i in range(5)  ]
        hours =["8:05","9:00","10:10","11:05","12:00","13:00","13:55","14:50","16:00","16:55","17:50"]
        #Formatage pour le calendrier que je comprend seulement quand je le regarde pendant très longtemps.
        #Quelques indications: on traite les données par ligne. C'est à dire par heures.
        #On cherche d'abord tout les cours valides, donc de la semaine prochaine.
        array = {}
        valid = onlyvalid()
        for hour in hours:
            sub = subselect(valid,hour)
            tmp = [hour,[None,None,None,None,None],[None,None,None,None,None]]
            for i in range(5):
                if(tmp[1][i]==None):
                    for elm in sub:
                        if(elm.day==jours_id[i][0]and elm.month==jours_id[i][1]):
                            if(search==None or (search==elm.slot.matiere)):
                                is_present = len(elm.students.all().filter(id=student.id))>0
                                tmp[1][i] = [elm.slot.matiere,elm.professor.nom,get_style_attribute(elm.slot.matiere),elm.professor.genre,elm.slot.room.name]
                                tmp[2][i] = [elm.places-len(elm.students.all()),elm.places,is_present,elm.id,get_style_attribute(elm.slot.matiere)]
            array[hour]=tmp
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
        context["crenaux"]= array
        context["first_day"]=formatted_day[0]
        context["last_day"]=formatted_day[-1]
        final_day = getFinalDayForInscription()
        context["final_day"]= "Vendredi "+str(final_day[0])+" "+getMonth(final_day[1])
        context["prof_url"] = "/prof/?identifiant="+token.UUID+"&tab=0"
        return render(request,'login/main-page.html',context)
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
    #Ajoute ou retire l'eleve aux élèves inscrits.
    if(has_student):
        current_class.students.remove(student)
    else:
        #Vérifie si il reste encore des places
        if(current_class.places>len(current_class.students.all())):
            current_class.students.add(student)
    #Redirection à l'url de départ
    return redirect(url)
def room(request):
    print(request.POST)
    if(not(len(request.POST)==11 or len(request.POST)==12)):
        return redirect(loginPage)
    post = request.POST
    salle = post.get("room")
    matiere_post= post.get("matiere")
    niveau = post.get("classe")
    day_post = post.get("day")
    hour_post = post.get("hour")
    size = post.get("size")
    option = post.get("option")
    prof = Token.objects.filter(UUID=post.get("token"))[0].student
    room_post= Room.objects.filter(name=salle)[0]
    slot_post = Slot(room=room_post,heure=convert_hour_to_int(hour_post),matiere=matiere_post)
    slot_post.save()
    day= convert_day_to_int(day_post)
    if(option=="post-week"):
        next_week_day_and_month = getNextWeek()[day]
        classe_day = next_week_day_and_month[0]
        classe_month = next_week_day_and_month[1]
        classe = Class(professor=prof,targeted_level=convert_niveau_to_int(niveau),places=size,month=classe_month,day=classe_day,slot=slot_post)
        classe.save()
    return redirect(request.POST.get("return"))

@csrf_protect
def prof(request):
    connection = connect(request)
    if connection.is_valid():
        tab = request.GET.get("tab",0)
        token = connection.token
        student = connection.student
        context = {}
        #Crée l'URL de la page
        url = ""
        uri = str(request.build_absolute_uri())
        index =0
        char =""
        while char!="?":
            char=uri[index]
            url+=char
            index+=1
        constructed_url=url+"identifiant="+token.UUID+"&tab="
        cours = [elm for elm in get_matiere()]
        tabs = ["Créer un cours","Vos cours"]
        urls = [(tabs[i],constructed_url+str(i)) for i in range(len(tabs))]
        context["urls"]=urls
        context["token"]=token.UUID
        context["prenom"]=student.prenom
        context["nom"]=student.nom
        context["retour"] = "/soutien/?identifiant="+token.UUID
        context["rooms"]= [room.name for room in Room.objects.all()]
        context["cours"]=cours
        context["classes"]= [get_classe(i) for i in range(5)]
        context["days"]= ["Lundi","Mardi","Mercredi","Jeudi","Vendredi"]
        context["hours"]= [convert_hour(i) for i in range(10)]
        next= format_next_monday()
        context["next_monday"]= next
        return render(request,'login/profs_content/prof_tab'+str(tab)+".html",context)
    else:
        return redirect(loginPage)