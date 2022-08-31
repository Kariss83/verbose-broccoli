from django import forms
from django.core.exceptions import ValidationError

CONTENT_TYPES = ['image']
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "10485760"


def file_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MiB.')

#
class UploadFileForm(forms.Form):
    file = forms.ImageField(validators=[file_size])
    
