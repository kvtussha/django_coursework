from django.forms import ModelForm

from main.models import Sending


class SendingForm(ModelForm):
    class Meta:
        model = Sending
        fields = ('status', 'message', 'start_date', 'end_date', 'frequency')
