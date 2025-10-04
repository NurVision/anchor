from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import activate


class UserLanguageMiddleware(MiddlewareMixin):
    """
    Custom middleware to activate user's preferred language from database.

    Priority order:
    1. User's saved language (in settings field)
    2. Django's LocaleMiddleware (Accept-Language header, cookie)
    3. Default language

    Add this AFTER LocaleMiddleware in settings.MIDDLEWARE
    """

    def process_request(self, request):

        if request.user.is_authenticated:
            user_settings = request.user.settings

            if user_settings and 'language' in user_settings:
                user_language = user_settings.get('language')

                if user_language in ['uz', 'ru', 'en']:
                    activate(user_language)
                    request.LANGUAGE_CODE = user_language
