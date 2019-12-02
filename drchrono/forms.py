from django import forms
from django.forms import widgets


# Add your forms here

class checkin_form(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}) )
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}) )
    social_security_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='if you don\'t have SSN, just leave it blank')

    def clean_social_security_number(self):
        ssn = self.cleaned_data['social_security_number']
        if ssn == '':
            return ssn

        chunks = ssn.split('-')
        valid=False
        if len(chunks) == 3:
            if len(chunks[0])==3 and len(chunks[1])==2 and len(chunks[2])==4:
                valid=True
        if not valid:
            raise forms.ValidationError('Please insert valid social security number(***-**-****)')
        return ssn


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.strip() == '':
            raise forms.ValidationError("Please insert first name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name.strip() == '':
            raise forms.ValidationError("Please insert last name")
        return last_name


class patient_info_form(forms.Form):
    gender = forms.ChoiceField(required=False, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], widget=forms.Select(attrs={'class': 'form-control'}))
    race = forms.ChoiceField(required=False, choices=[('blank', ''), ('indian', 'American Indian or Alaska Native'), ('asian', 'Asian'),
                                    ('black', 'Black or African American'), ('hawaiian', 'Native Hawaiian or Other Pacific Islander'),
                                    ('white', 'White'), ('other', 'Other Race'),
                                    ('declined', 'Decline to specify')], widget=forms.Select(attrs={'class': 'form-control'}))
    social_security_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), 
        error_messages={
            'invalid': 'Please insert a valid date in the format yyyy-mm-dd'
        })
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_social_security_number(self):
        ssn = self.cleaned_data['social_security_number']
        if ssn == '':
            return ssn

        chunks = ssn.split('-')
        valid=False
        if len(chunks) == 3:
            if len(chunks[0])==3 and len(chunks[1])==2 and len(chunks[2])==4:
                valid=True
        if not valid:
            raise forms.ValidationError('Please insert valid social security number(***-**-****)')
        return ssn

    # write cell phone constraints and home phone
    # add ethnicity field
    # add state and zip code info
