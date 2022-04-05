from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, Textarea, \
    ModelMultipleChoiceField, CharField, UUIDField
from django.urls import reverse_lazy

from .models import Election, Candidate, Ticket

MD_INPUT_SAFE = {
    'class': 'markdown-input',
    'data-endpoint': reverse_lazy('utilities:preview_safe'),
}

MD_INPUT_TEXT = {
    'class': 'markdown-input',
    'data-endpoint': reverse_lazy('utilities:preview_safe'),
}


class ElectionForm(ModelForm):
    class Meta:
        model = Election
        fields = ['name', 'description', 'vote_type',
                  'max_votes', 'seats', 'open']
        widgets = {'description': Textarea(attrs=MD_INPUT_SAFE)}


class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'description', 'state']
        widgets = {'description': Textarea(attrs=MD_INPUT_TEXT)}


class IDTicketForm(Form):
    ids = CharField(help_text="A list of whitespace separated uni-ids",
                    widget=Textarea(), label="IDs")
    elections = ModelMultipleChoiceField(Election.objects.filter(archived=False))


class DeleteTicketForm(Form):
    elections = ModelMultipleChoiceField(
        Election.objects.filter(archived=False, open=False))


class NullForm(Form):
    pass


class ResetVoteForm(Form):
    uuid = UUIDField(label="Ticket UUID")

    def clean_uuid(self):
        uuid_value = self.cleaned_data['uuid']
        if not Ticket.objects.filter(spent=True, uuid=uuid_value).exists():
            raise ValidationError("Incorrect UUID")
        return uuid_value
