import hashlib
from .models import Student,Class
from random import randint
from datetime import date, timedelta
hours = ["8h05","9h00","10h10","11h05","12h00","13h00","13h55","14h50","16h00","16h55","17h50"]
niveaux = ["Seconde","Première","Terminale","BTS 1ère Année","BTS 2ème Année","Sans-Classe"]
def get_style_attribute(matiere:str):
    a =matiere.upper()
    for elt in get_matiere():
        if(a==elt[0].upper()):
            return elt[1]
    return "#777777"
def get_matiere():
    a= [("Physique-Chimie","#1e81b0"),("Mathématiques","#fdfc1a"),("Maths-Expertes","#fdfc1a"),("Maths-Complémentaire","#fdfc1a"),("Anglais","#9925be")]
    return a
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
def get_student(id:int):
    query = Student.objects.filter(identifiant=id)
    return query[0]
def createUUID():
    data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ0123456789"
    char = ''
    for i in range(20):
        char = char + data[randint(0,len(data)-1)]
    return char
def convert_hour(id:int):
    return hours[id]
def convert_serie(chars:str):
    array = {"gen":"Générale","per":"Personnel Enseignant"}
    return array.get(chars,"")
def get_classe(i:int):
    if(i==-1):
        return ""
    return niveaux[i]
def convert_niveau_to_int(niveau:str):
    return niveaux.index(niveau)
def getMonth(i:int):
    months= ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    return months[i]
def getNextWeek():
    today = date.today()
    start = today - timedelta(days=(today.weekday()+2)%7)+timedelta(days=9)
    liste = [((start+timedelta(days=i)).day,(start+timedelta(days=i)).month -1) for i in range(5)]
    return liste	
def getFinalDayForInscription():
    today = date.today()
    last = today - timedelta(days=(today.weekday()+2 )%7)+timedelta(days=6)
    return (last.day,last.month)
def getNextWeekYear():
    today = date.today()
    last = today - timedelta(days=(today.weekday()+2 )%7)+timedelta(days=6)
    return last.year
def format_next_monday():
    monday = getNextWeek()[0]
    month = str(monday[1]+1)
    day = str(monday[0])
    if(len(month)==1):
        month ="0"+month
    if(len(day)==1):
        day= "0"+day 
    return str(getNextWeekYear())+"-"+month+"-"+day
def convert_day_to_int(day:str):
    a = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
    return a.index(day)
def convert_hour_to_int(hour:str):
    return hours.index(hour)
def subselect(array,hour):
    sub = []
    for elm in array:
        if(hours[elm.slot.heure].replace("h",":")==hour):
            sub.append(elm)
    return sub
def onlyvalid():
    classes = Class.objects.all()
    jours_id= getNextWeek()
    valid = []
    for cour in classes:
        for jour in jours_id:
            if(cour.day==jour[0] and cour.month==jour[1]):
                valid.append(cour)
                break;
    return valid
