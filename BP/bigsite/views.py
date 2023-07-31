import sys, os
 
sys.path.append(os.path.dirname(os.path.abspath("C:\\Users\\User\\Documents\\GitHub\\one-one-project\\BP")))
from static.python.render_support import *
from user.models import User

def index(request):
    user_count = User.objects.count() 
    data = {
        "count" : format(user_count+300000, ",")
    }  
    return n_render(request,'main/index.html', data)

def about(request):
    return n_render(request,'main/about.html')
    