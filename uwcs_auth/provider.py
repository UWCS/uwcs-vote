from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class UWCSAccount(ProviderAccount):
    def to_str(self):
        dflt = super(UWCSAccount, self).to_str()
        return self.account.extra_data.get("nickname", dflt)


class UWCSProvider(OAuth2Provider):
    id = "uwcs"
    name = "UWCS"
    account_class = UWCSAccount

    def extract_uid(self, data):
        return data["sub"]

    def extract_common_fields(self, data):
        user = data["user"]
        return dict(
            uni_id=user.get("uni_id"),
            email=user.get("email"),
            nickname=data.get("preferred_username"),
            first_name=user.get("given_name"),
            last_name=user.get("family_name"),
        )

    def get_default_scope(self):
        return ["profile", "email", "openid"]


provider_classes = [UWCSProvider]
