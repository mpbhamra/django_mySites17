
from django import forms
from myApp.models import Topics,Student

class TopicForm(forms.ModelForm):
    subject = forms.CharField(label='Subject', max_length=100, required=False)
    intro_course = forms.BooleanField(label='This should be an introductory level course', required=False)

    avg_age = forms.IntegerField(label="What is Your Age")
    class Meta:
        model = Topics
        fields = '__all__'
        widgets = {
            'time': forms.RadioSelect(attrs={'class':'radio'}) ,

        }

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name','last_name','email','username','password','address','city','province','age','picture')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'})
        }




class InterestForm(forms.Form):
    CHOICES = (('1', 'Yes',), ('0', 'No',))
    interested = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
    age = forms.IntegerField(initial=20, label="Age of Use")
    comments = forms.Textarea(attrs={'required':'false'})
    comments.id_for_label('Additional Conditions')



class UploadImageForm(forms.Form):
    title = forms.CharField( max_length=100)
    imgfile = forms.ImageField()