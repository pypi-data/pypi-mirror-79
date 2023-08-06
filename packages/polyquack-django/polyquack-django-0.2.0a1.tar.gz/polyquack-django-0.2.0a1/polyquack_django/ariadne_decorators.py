"""
Some useful decorators for use with Ariadne GraphQL.
"""

from django.utils import translation


def translate_resolved_to_request_language(resolver):
    """
    This decorator wraps a resolver function that returns a Translatable instance,
    and gets the appropriate translation for the request's language (according to 
    Django's rules).
    """

    def wrapper_translate(*args, **kwargs):
        _, info, *__ = args
        resolved = resolver(*args, **kwargs)
        return resolved.translate(
            translation.get_language_from_request(info.context["request"])
        )

    return wrapper_translate
