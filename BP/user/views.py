from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from user.forms import UserForm
from user.models import user_favor
from static.python.render_support import *
from .forms import EditProfileForm, UserFavorForm
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import JsonResponse
import re, hashlib

User = get_user_model()

def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False            
            user.save()
            # 이메일 인증 URL 생성
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_url = request.build_absolute_uri(f'/activate/{uid}/{token}/')

            # 인증 이메일 전송
            email_subject = '책크미 계정을 인증해주세요'
            email_body = f'다음 링크를 클릭해 책크미 계정을 인증해주세요: {activation_url}'
            from_email = 'noreply@chaekme.com'
            email = EmailMessage(email_subject, email_body, from_email=from_email, to=[form.cleaned_data['email']])
            email.send()

                
            return n_render(request, 'user/active_required.html', {'email':user.email})# 회원가입 성공
    else:
        form = UserForm()
        
    
        
    data = {
        "form" : form,
    }
        
    return n_render(request, 'user/register.html', {"form": form})      # 회원가입 실패

def check_username(request): #아이디 중복 확인
    errorname = "couldn't get"
    try:
        username = request.GET['username']
        errorname = "couldn't sql"
        if username:
            exists = User.objects.filter(username=username).exists()
            errorname = "couldn't return"
            return JsonResponse({'exists': exists})
    except:
        return JsonResponse({'error': errorname})

#이메일 인증 URL 접근 > is_active 활성화 뷰
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return n_render(request, 'user/active_response.html', {'username':user.username})  # 계정 활성화 성공
    else:
        return redirect('user:login')  # 계정 활성화 실패

#로그인 처리 뷰
def login_view(request):
    #로그인 폼 제출 시
    if request.method == 'POST':
        username = request.POST['username']
        password = hashlib.sha256(request.POST['password'].encode()).hexdigest()
        # 사용자 인증
        user = authenticate(request, username=username, password=password)
        if user is not None:  #로그인 성공
            login(request, user=user)
            request.session['id'] = str(user)
            return redirect('main')
        else: #로그인 실패
            return n_render(request, 'user/login.html', {'error': '아이디 혹은 비밀번호 오류입니다.'})
    #초기 페이지
    else:
        return n_render(request, 'user/login.html')

def select(request):
    #선호 장르 4개 선택지 제출할 경우
    if request.method == "POST":
        username = str(request.user)
        genres = request.POST['summary'].split('|||')
        try:
            form = user_favor.objects.get(username=username)
        except user_favor.DoesNotExist:
            form = None
        
        form_data = {
            'username': username,
            'favor1': genres[0],
            'favor2': genres[1],
            'favor3': genres[2],
            'favor4': genres[3]
        }
        if form:
            form = UserFavorForm(data=form_data, instance=form)
        else:
            form = UserFavorForm(data=form_data)
        if form.is_valid():
            form.save()
            return redirect('main')
    #초기 페이지
    novel = []
    novel.append(["한국", "50917"])
    novel.append(["일본", "50918"])
    novel.append(["영미", "50919"])
    novel.append(["스페인/중남미", "50920"])
    novel.append(["프랑스", "50921"])
    novel.append(["독일", "50922"])
    novel.append(["중국", "50923"])
    novel.append(["러시아", "52650"])
    novel.append(["세계", "50925"])
    novel.append(["추리/미스터리", "50926"])
    novel.append(["판타지/환상문학", "50928"])
    novel.append(["역사", "50929"])
    novel.append(["과학(SF)", "50930"])
    novel.append(["호러/공포", "50931"])
    novel.append(["무협", "50932"])
    novel.append(["액션/스릴러", "50933"])
    novel.append(["로맨스", "50935"])
    
    essay = []
    essay.append(["한국", "51371"])
    essay.append(["외국", "51373"])
    essay.append(["동물", "174700"])
    essay.append(["명상", "51374"])
    essay.append(["심리치유", "51375"])
    essay.append(["사진/그림", "51376"])
    essay.append(["음식", "180236"])
    essay.append(["여행", "51377"])
    essay.append(["독서", "51380"])
    essay.append(["예술", "51842"])
    essay.append(["종교", "51389"])
    essay.append(["사랑/연애", "51391"])
    essay.append(["노년", "51392"])
    essay.append(["자연", "51394"])
    essay.append(["명언/잠언록", "51398"])
    essay.append(["일기/편지", "51402"])
    essay.append(["유머/풍자/우화", "51404"])
    essay.append(["포켓", "51408"])
    essay.append(["작은 이야기 모음", "51413"])
    essay.append(["명사", "51416"])
    
    self = []
    self.append(["성공", "70214"])
    self.append(["리더십", "70212"])
    self.append(["행복론", "70211"])
    self.append(["인간관계", "2951"])
    self.append(["힐링", "70236"])
    self.append(["심플라이프", "107822"])
    self.append(["협상/설득/화술", "70224"])
    self.append(["프레젠테이션", "70233"])
    self.append(["기획/보고", "70228"])
    self.append(["시간/정보관리", "70220"])
    self.append(["두뇌계발", "70223"])
    self.append(["취업/진로", "2943"])
    self.append(["20대의 자기계발", "70241"])
    self.append(["여성의 자기계발", "70218"])
    self.append(["중년의 자기계발", "70219"])
    
    data = {
        "novels":novel,
        "essays":essay,
        "selfs":self,
    }
    return n_render(request, 'user/select.html', data)

def edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:mypage')
    else:
        form = EditProfileForm(instance=request.user)
    
    return n_render(request, 'user/edit.html', {'form': form})

def change_password(request):  
    if request.user.is_anonymous:
        redirect('main')
    username = request.user.username
    if request.method == 'POST' and request.POST.get('password1') is not None:
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return n_render(request, 'user/change_password.html', {'error': '패스워드 확인이 일치하지 않습니다.'})
        elif len(password1) < 8:
            return n_render(request, 'user/change_password.html', {'error': '비밀번호는 숫자, 문자, 특수문자를 포함해 8자리 이상이어야 합니다.'})
        elif not re.search(r'\d', password1) or not re.search(r'[a-zA-Z]', password1) or not re.search(r'[^a-zA-Z0-9]', password1):
            return n_render(request, 'user/change_password.html', {'error': '비밀번호는 숫자, 문자, 특수문자를 포함해 8자리 이상이어야 합니다.'})
        hashed_password = hashlib.sha256(password1.encode()).hexdigest()
        user = User.objects.get(username=request.user.username)
        user.password = hashed_password
        user.save()
        if user is not None:
            user = authenticate(request, username=username, password=hashed_password)
            login(request, user=user)
        return redirect('user:mypage')
    else:
        return n_render(request, 'user/change_password.html')

def delete_check(request):
    return n_render(request, 'user/delete_check.html', login_essential=1)

def delete_real(request):
    if request.method == 'POST':
        user = request.user
        if user:
            user.delete()
            return redirect('user:logout')
    return redirect('user:delete_real')

def mypage(request):
    return n_render(request,'user/mypage.html', login_essential=1)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            pass
        else:        
            if sociallogin.account.provider=='kakao':
                email = sociallogin.account.extra_data['kakao_account']['email']
            elif sociallogin.account.provider=='google':
                email = sociallogin.account.extra_data['email']
            else:
                email = None
            if email:
                existing_user = User.objects.filter(email=email).first()
                if existing_user:
                    if not existing_user.is_active:
                        existing_user.is_active = 1
                        existing_user.save()
                    sociallogin.connect(request, existing_user)
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # 사용자 정보 처리 및 User 모델에 저장 로직 추가
        user.is_active=1
        if sociallogin.account.provider == 'google':
            # 구글 로그인인 경우
            user.name = sociallogin.account.extra_data['name']
            user.nickname = sociallogin.account.extra_data['name']
            user.email = sociallogin.account.extra_data['email']
        elif sociallogin.account.provider == 'kakao':
            # 카카오 로그인인 경우
            if 'username' in data:
                if data['username']:
                    user.name = data['username']
            if 'profile_image' in data:
                if data['profile_image']:
                    user.img_src = data['profile_image']
            if 'email' in data:
                if data['email']:
                    user.email = data['email']
        return user

def forgot_id(request):
    if 'email' not in request.POST:#초기 페이지
        return n_render(request, 'user/forgot_id.html')
    email = request.POST.get('email')
    users = User.objects.filter(email=email)
    if users.exists():  #입력한 email에 맞는 아이디가 존재할 경우
        subject = '가입하신 아이디를 알려드립니다.'
        message = '가입하신 아이디 목록\n\n' + ',   '.join([user.username for user in users])
        from_email = 'noreply@chaekme.com'
        email = EmailMessage(subject, message, from_email, to=[email])
        email.send()
        return n_render(request, 'user/forgot_id_email.html')
    else:               #입력한 email에 맞는 아이디가 존재하지 않을 경우
        return n_render(request, 'user/forgot_id.html', {'error':'이메일이 존재하지 않습니다.'})
    
def forgot_pw(request, uid=None, token=None):
    if 'username' not in request.POST:  # 초기 페이지
        return n_render(request, 'user/forgot_pw.html')
    if uid is not None and token is not None: #인증된 메일URL로 접근하면 비밀번호 변경 페이지로 연결
        uid = force_bytes(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            request.user = user
            return redirect('user:change_password')
    if User.objects.filter(username=request.POST.get('username')).exists(): #입력한 username이 존재할 경우
        user = User.objects.get(username=request.POST.get('username'))
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        change_pw_url = request.build_absolute_uri(f'/user/forgot_pw/{uid}/{token}/')
        email_subject = '비밀번호 초기화 안내'
        email_body = f'비밀번호 초기화를 위한 링크입니다. : {change_pw_url}'
        email = EmailMessage(email_subject, email_body, to=[user.email])
        email.send()
        return n_render(request, 'user/forgot_pw_email.html')
    else:                                                                   #입력한 username이 존재하지 않을 경우
        return n_render(request, 'user/forgot_pw.html', {'error' : 'ID가 존재하지 않습니다.'})
