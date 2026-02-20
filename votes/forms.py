import django as django
from django.core.exceptions import ValidationError
from django.forms import (
    CharField,
    DateTimeField,
    Form,
    ModelForm,
    ModelMultipleChoiceField,
    Textarea,
    UUIDField,
)
from django.urls import reverse_lazy

from .models import Candidate, Election, Ticket

MD_INPUT_SAFE = {
    "class": "markdown-input",
    "data-endpoint": reverse_lazy("utilities:preview_safe"),
}

MD_INPUT_TEXT = {
    "class": "markdown-input",
    "data-endpoint": reverse_lazy("utilities:preview_safe"),
}


class CommaSeparatedListField(CharField):
    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(",") if item.strip()]

    def prepare_value(self, value):
        if isinstance(value, list):
            return ", ".join(value)
        return value


class ElectionForm(ModelForm):
    class Meta:
        model = Election
        fields = [
            "name",
            "description",
            "vote_type",
            "max_votes",
            "seats",
            "open",
            "self_id_eligibility_confirmation",
            "required_webgroups",
        ]
        widgets = {
            "description": Textarea(attrs=MD_INPUT_SAFE),
            "self_id_eligibility_confirmation": Textarea(attrs=MD_INPUT_SAFE),
        }

    required_webgroups = CommaSeparatedListField(
        help_text="Required webgroups to be eligible to vote, separated by commas (e.g. all-block-1, all-postgraduates)",
        required=False,
    )


class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "description", "state"]
        widgets = {"description": Textarea(attrs=MD_INPUT_TEXT)}


class IDTicketForm(Form):
    ids = CharField(
        help_text="A list of whitespace separated uni-ids",
        widget=Textarea(),
        label="IDs",
    )
    elections = ModelMultipleChoiceField(Election.objects.filter(archived=False))


class DateTimeInput(django.forms.DateTimeInput):
    input_type = "datetime-local"


class DeleteTicketForm(Form):
    elections = ModelMultipleChoiceField(
        Election.objects.filter(archived=False, open=False)
    )


class NullForm(Form):
    pass


class ResetVoteForm(Form):
    uuid = UUIDField(label="Ticket UUID")

    def clean_uuid(self):
        uuid_value = self.cleaned_data["uuid"]
        if not Ticket.objects.filter(spent=True, uuid=uuid_value).exists():
            raise ValidationError("Incorrect UUID")
        return uuid_value
