from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'url']

    def clean(self):
        print('clean called')
        cleaned_data = super().clean()
        file = cleaned_data.get("video_file")
        url = cleaned_data.get("url")

        if not file and not url:
            raise forms.ValidationError("Provide at least a file or a URL.")

        if file and url:
            raise forms.ValidationError("Provide only one: file or URL.")