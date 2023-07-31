from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def n_render(request, html, value = {}, login_essential = 0):
    '''
    로그인 여부 확인 및 세션값 data 로 추가,
    argument 설명
    request : request 를 그대로 render() 에 넘겨줌  *필수
    html : html url 을 그대로 render() 에 넘겨줌    *필수
    value : 해당 페이지에서 표시하는데 필요한 data 를 받아줌    *default {}
    login_essential : 로그인 필수 여부, 필수 일 시 
    로그인 판단 후 login 페이지로 리다이렉트           *default 0
    '''
    if request.user.is_authenticated:
        current_id = str(request.user)
    else:
        current_id = ''
        
    # try:
    #     current_id = request.session['id']
    # except:
    #     current_id = ''
        
    value.update({'id' : current_id})
    
    alert = ''
    try:
        alert = request.GET.get('alert')
    except:
        alert = ''
    if alert == None:
        alert = ''
    value.update({'alert' : alert})
    
    if login_essential and current_id == '':
        return HttpResponseRedirect(reverse('user:login') + "?alert=로그인 이후에 이용하실 수 있습니다.")
    
    return render(request, html, value)
