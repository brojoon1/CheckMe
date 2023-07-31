from django import forms

class BookSearchForm(forms.Form) :
    search_query = forms.CharField(label = "책 검색")