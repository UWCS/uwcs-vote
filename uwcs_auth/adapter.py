from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

from uwcs_auth.models import WarwickVoteUser


class WarwickVoteUserAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if request.path.rstrip("/") == reverse("account_signup").rstrip("/"):
            return False
        return True

    def save_user(self, request, user, form, commit=True):
        # Add the first and last names to the user
        user = super(WarwickVoteUserAccountAdapter, self).save_user(
            request, user, form, commit=False
        )
        user.username = form.cleaned_data.get("email")
        user.first_name = form.cleaned_data.get("given_name")
        user.last_name = form.cleaned_data.get("family_name")
        user.save()

        # Create the associated profile model
        user_profile = WarwickVoteUser(
            user=user,
            uni_id=form.cleaned_data.get("uni_id"),
            nickname=form.cleaned_data.get("preferred_username"),
        )
        user_profile.save()


class UWCSUserAccountAdapter(DefaultSocialAccountAdapter):
    def get_signup_form_initial_data(self, sociallogin):
        user = sociallogin.user

        initial = {
            "username": user_email(user) or "",
            "email": user_email(user) or "",
            "uni_id": sociallogin.account.extra_data.get("uni_id", ""),
            "nickname": sociallogin.account.extra_data.get("preferred_username", ""),
            "first_name": user_field(user, "given_name") or "",
            "last_name": user_field(user, "family_name") or "",
        }

        return initial

    def save_user(self, request, sociallogin, form=None):
        user = super(UWCSUserAccountAdapter, self).save_user(request, sociallogin, form)

        initial = self.get_signup_form_initial_data(sociallogin)

        # Create the associated profile model
        user_profile = WarwickVoteUser(
            user=user,
            uni_id=initial.get("uni_id"),
            nickname=initial.get("nickname"),
        )
        user_profile.save()
