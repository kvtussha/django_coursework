from django.forms import ModelForm

from main.models import Mailing


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ('status', 'message', 'start_date', 'end_date', 'frequency')
