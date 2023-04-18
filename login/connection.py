import datetime
from .models import Token
class Connection:
    def __init__(self,token,student):
        self.token=token
        self.student=student
    def getTimeSinceToken(self):
        token = self.token
        return ((datetime.datetime.now(datetime.timezone.utc)-token.creation_date))/ datetime.timedelta(seconds=1)
    def is_valid(self):
        if self.token==None or self.student==None:
            return False
        else:
            return self.getTimeSinceToken()<30*60
invalid_connection = Connection(None,None)


def connect(request):
    query = request.GET.get('identifiant',None)
    if(query==None):
        return invalid_connection
    #Recherche des tokens avec cet identifiant (Normalement y'en a qu'un)
    a = Token.objects.filter(UUID=query)
    if(a.count()<1):
        return invalid_connection
    else:
        token = a[0]
        student = token.student
        return Connection(token,student)
