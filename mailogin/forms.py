from django import forms
from .models import MyUser,Project


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control',
                             'placeholder': 'Email Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                'placeholder': 'Create Password'}), error_messages={'required': "Please enter your password"})
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                'placeholder': 'Re-enter Password'}), error_messages={'required': "Please enter your password"})

    user_type = forms.ChoiceField(choices={
        ("A", "Applicant"),
        ("E", "Employer"),
        ("S", "Staff"),
        }, widget=forms.RadioSelect(), initial="A")

    class Meta:
        model = MyUser
        fields = ('email', 'user_type')

    def __init__(self, *args, **kwargs):

        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False

    def clean_email(self):
        email = self.cleaned_data['email']
        #self.cleaned_data['username'] = email
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email %s is already in use" % (email))
        return email

    def clean_password2(self):
        """Checks two password entries match.
        """
        cleaned_data = super(UserCreationForm, self).clean() #to see the password validation
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # if len(password1) <= 4 or len(password2) <= 4:
        #     raise forms.ValidationError("Password must be at least 5 characters long")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
                # del cleaned_data["password1"]  #to delete the invalid password, not necessary
                # del cleaned_data["password2"]
        return password2

    def save(self, commit=True):
        """Saves the provided password in hashed format.
        """
        user = super(UserCreationForm, self).save(commit=False)
        # get the user object first, then add password, then save
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = True
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control',
                             'placeholder': 'Your email address'}), error_messages={'required': "Please enter your email id"})
                           # widget=forms.widgets.TextInput
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                               'placeholder': 'Your password'}), error_messages={'required': "Please enter your password"})
                            # widget=forms.widgets.PasswordInput

    class Meta:
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['password'].label = False


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Project Name'}),
            'startdate': forms.DateInput(attrs={'class': 'form-control datepicker','placeholder':'Start Date'}),
            'endate': forms.DateInput(attrs={'class': 'form-control datepicker','placeholder':'End Date'})
        }



