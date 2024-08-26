from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Country, Client, City, State, Testimonial
from django.urls import reverse_lazy


class ClientRegistrationForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']


    def __init__(self, *args, **kwargs):
        super(ClientRegistrationForm, self).__init__(*args, **kwargs)
        
        # Update widget attributes for placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Pick a unique Username', 'style':'border: 1px solid #ddd'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter a strong Password', 'style':'border: 1px solid #ddd'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Enter the same Password', 'style':'border: 1px solid #ddd'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter a valid Email address - -example@yahoomail.com', 'style':'border: 1px solid #ddd'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your First Name', 'style':'border: 1px solid #ddd'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name', 'style':'border: 1px solid #ddd'})   
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # check if Client object exists or Create the Client object
            if not Client.objects.filter(user=user).exists():

                client = Client.objects.create(
                    user=user,
                )
            
            client.save()
        return user


class UpdateUserInfoForm(UserChangeForm):
    # Get rid of the password Hash issue
    password = None
    username = forms.CharField(label="Username:", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pick a unique Username', 'style':'border: 1px solid #ddd'}), required=True)
    email = forms.EmailField(label="Email:", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter a valid Email address - -example@yahoomail.com', 'style':'border: 1px solid #ddd'}), required=False)
    first_name = forms.CharField(label="First Name:", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'style':'border: 1px solid #ddd'}), required=False)
    last_name = forms.CharField(label="Last Name:", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'style':'border: 1px solid #ddd'}), required=False)
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UpdateProfilezzForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['country', 'state', 'city', 'occupation', 'gender', 'avatar'] 

        widgets = {
            'occupation': forms.TextInput(attrs={'style':'border: 1px solid #ddd'}),
            'gender': forms.Select(attrs={'style':'border: 1px solid #ddd'}),            
            'country': forms.Select(attrs={'id': 'country', 'class': 'form-control', 'style':'border: 1px solid #ddd'}),
            'state': forms.Select(attrs={'id': 'state', 'class': 'form-control',
                                        'state-queries-url': reverse_lazy('ajax_load_states'), 'style':'border: 1px solid #ddd'}),
            'city': forms.Select(attrs={'id': 'city', 'class': 'form-control',
                                        'city-queries-url': reverse_lazy('ajax_load_cities'), 'style':'border: 1px solid #ddd'}),   
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProfilezzForm, self).__init__(*args, **kwargs)

        # Handle dynamic queryset for state and city fields based on country and state selection
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass # invalid input from the client will be ignored and fallback to an empty queryset state
                
        elif self.instance.pk and self.instance.country is not None:
             self.fields['state'].queryset = self.instance.country.states.order_by('name')

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')  
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.state is not None:
            self.fields['city'].queryset = self.instance.state.cities.order_by('name')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['country', 'state', 'city', 'occupation', 'gender', 'avatar'] 

        widgets = {            
            'country': forms.Select(attrs={
                'id': 'country', 
                'class': 'form-control',
                'hx-get': "{% url 'ajax_load_states' %}",
                'hx-target': '#id_state',
                'hx-trigger': 'change',
            }),
            'state': forms.Select(attrs={
                'id': 'state', 
                'class': 'form-control',
                'hx-get': "{% url 'ajax_load_cities' %}",
                'hx-target': '#id_city',
                'hx-trigger': 'change',
            }),
            'city': forms.Select(attrs={
                'id': 'city', 
                'class': 'form-control',
            }),
            'occupation': forms.TextInput(attrs={'style':'border: 1px solid #ddd'}),
            'gender': forms.Select(attrs={'style':'border: 1px solid #ddd'}),    
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if self.instance.pk and self.instance.country:
            self.fields['state'].queryset = State.objects.filter(country=self.instance.country).order_by('name')
        if self.instance.pk and self.instance.state:
            self.fields['city'].queryset = City.objects.filter(state=self.instance.state).order_by('name')

class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['testifier', 'testimony', 'photo', 'occupation']

        widgets = {
            'testifier': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your name', 
                'style':'border: 1px solid #ddd'
            }),
            'testimony': forms.TextInput(attrs={
                'class':'form-control', 
                'placeholder':'Let us know how you feel about PAY-T', 
                'style':'border: 1px solid #ddd'
            }),
            'Occupation': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your occupation', 
                'style':'border: 1px solid #ddd'
            }),
        }