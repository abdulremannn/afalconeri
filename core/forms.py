from django import forms

INQUIRY_CHOICES = [
    ('', 'Select Inquiry Type'),
    ('defense_systems', 'Defense Systems'),
    ('surveillance', 'Surveillance Solutions'),
    ('uav_procurement', 'UAV Procurement'),
    ('partnership', 'Strategic Partnership'),
    ('civil_applications', 'Civil Applications'),
    ('media', 'Media & Press'),
    ('other', 'Other'),
]

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name',
            'autocomplete': 'off',
        })
    )
    organization = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Organization / Entity',
            'autocomplete': 'off',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Official Email Address',
            'autocomplete': 'off',
        })
    )
    inquiry_type = forms.ChoiceField(
        choices=INQUIRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your inquiry...',
            'rows': 6,
        })
    )
