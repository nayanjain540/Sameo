from django import forms

CATEGORY_CHOICES = [
    ('VIDEO_GAME', 'Video Game'),
    ('KIDS_CAMERA', 'Kids Camera'),
    ('FITNESS_GAME', 'Fitness Game'),
]

VIDEO_TYPE_CHOICES = [
    ('HAND_VIDEO_GAME', 'Hand Video Game'),
    ('TV_VIDEO_GAME', 'TV Video Game'),
]

HAND_VIDEO_MODELS = [
    ('KidsGear', 'KidsGear'),
    ('DreamBoy', 'DreamBoy'),
    ('GameGear', 'GameGear'),
    ('Thunder NX', 'Thunder NX'),
    ('Xtreme Pro', 'Xtreme Pro'),
    ('SG9000', 'SG9000'),
]

TV_VIDEO_MODELS = [
    ('Little Master', 'Little Master'),
    ('Micro Genius', 'Micro Genius'),
    ('Ultrazone', 'Ultrazone'),
    ('Ultrazone HD', 'Ultrazone HD'),
    ('Micro Lite', 'Micro Lite'),
    ('iPlay (without Gun)', 'iPlay (without Gun)'),
    ('Micro Thunder', 'Micro Thunder'),
    ('iPlay Plus (with Gun)', 'iPlay Plus (with Gun)'),
]

KIDS_CAMERA_MODELS = [
    ('SKC-P10', 'SKC-P10'),
    ('SKC-0030', 'SKC-0030'),
    ('SKC-Q5', 'SKC-Q5'),
]

FITNESS_MODELS = [
    ('Gym Master', 'Gym Master'),
]

PLATFORM_CHOICES = [
    ('Online', 'Online'),
    ('Offline', 'Offline'),
]

class WarrantyForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    video_type = forms.ChoiceField(choices=VIDEO_TYPE_CHOICES, required=False)
    model = forms.ChoiceField(choices=[], required=False)
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES)
    site_name = forms.CharField(required=False, label='Site Name')
    shop_name = forms.CharField(required=False, label='Shop Name')
    serial_number = forms.CharField(required=False, label='Serial Number')
    date_of_purchase = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    invoice = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(WarrantyForm, self).__init__(*args, **kwargs)
        self.fields['model'].choices = HAND_VIDEO_MODELS + TV_VIDEO_MODELS + KIDS_CAMERA_MODELS + FITNESS_MODELS
