from django import forms
from user.models import User, user_favor
import hashlib
from django.contrib.auth.forms import UserChangeForm
import re

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email_front = forms.CharField(label='이메일')
    domain_choice = forms.ChoiceField(
        label='도메인 선택',
        choices=[('custom', '직접입력'), ('naver.com', 'naver.com'), ('gmail.com', 'gmail.com')],
        initial='직접입력'
    )
    custom_domain = forms.CharField(label='직접입력', required=False)

    class Meta:
        model = User
        fields = ['username', 'phone', 'email_front', 'custom_domain', 'name', 'nickname', 'birth', 'gender']
        
    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        if password1 is None:
            True #already print error
        else:
            if len(password1) < 8:
                self.add_error("password1", "비밀번호는 8글자 이상이어야 합니다.")
            if not re.search(r'\d', password1) or not re.search(r'[a-zA-Z]', password1) or not re.search(r'[^a-zA-Z0-9]', password1):
                self.add_error("password1", "숫자, 문자, 특수문자를 각각 하나 이상 포함해야 합니다.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        #비밀번호 예외처리
        password1 = self.clean_password()
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "비밀번호 확인이 일치하지 않습니다.")
        #이메일 예외처리
        email_front = self.cleaned_data.get('email_front')
        domain_choice = self.cleaned_data.get('domain_choice')
        custom_domain = self.cleaned_data.get('custom_domain')
            
        if domain_choice != 'custom':
            custom_domain = domain_choice
        cleaned_data['email'] = str(email_front) + '@' + str(custom_domain)
        email = self.cleaned_data.get('email')
        
        if email_front is None:
            True #already print error
        elif custom_domain == "":
            self.add_error('email_front', '도메인을 입력해주세요.')
        elif '.' not in custom_domain or custom_domain.split('.')[1] == '':
            self.add_error('email_front', '잘못된 도메인 형식입니다.')
        return cleaned_data
  
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = hashlib.sha256(self.cleaned_data.get('password1').encode()).hexdigest()
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        
        return user

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['phone', 'nickname', 'name']
    
    
class UserFavorForm(forms.ModelForm):
    class Meta:
        model = user_favor
        fields = ['username', 'favor1', 'favor2', 'favor3', 'favor4']