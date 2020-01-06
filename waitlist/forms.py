from django import forms
from django.forms import widgets
import waitlist.models as gm


class WaitListForm(forms.ModelForm):
    email = forms.EmailField()
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    location = forms.CharField(max_length=100)

    class Meta:
        model = gm.WaitList
        fields = ('firstname', 'email', 'lastname', 'location' )

    firstname.widget.attrs.update({'class': 'form-control',
                                  'placeholder': 'Enter firstname'})
    lastname.widget.attrs.update({'class': 'form-control',
                                  'placeholder': 'Enter lastname'})
    location.widget.attrs.update({'class': 'form-control',
                                  'placeholder': 'Enter location'})
    email.widget.attrs.update({'class': 'form-control',
                               'placeholder': 'Enter email'})
