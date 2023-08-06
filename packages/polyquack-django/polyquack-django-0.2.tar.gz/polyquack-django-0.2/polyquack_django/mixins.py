from typing import Optional

from django.conf import settings
from django.db import models
from polyquack.translation import Translatable


class TranslatableModel(models.Model):
    """
    Model with translatable fields.

    Fields should be listed as an iterable (like set, list, tuple) inside the
    translatable_fields attribute. E.g.:
        translatable_fields = {"title", "text"}
    """

    translatables = models.JSONField(default=dict)

    def __init_subclass__(cls, **kwargs):
        """Verify that derived classes have a translatable_fields attribute."""
        if not hasattr(cls, "translatable_fields"):
            raise AttributeError(f"'translatable_fields' attribute not found in {cls}")
        super().__init_subclass__(**kwargs)

    def __getattr__(self, name) -> Optional[Translatable]:
        """If attr is a translatable field, return a Translatable object."""
        try:
            if name in self.translatable_fields:
                code = (
                    settings.LANGUAGE_CODE
                    if hasattr(settings, "LANGUAGE_CODE")
                    else None
                )
                return Translatable(translations=self.translatables[name], default=code)
        except KeyError:
            # Don't raise KeyError as we're trying to get an attribute
            pass

        # The attribute was not a class instance attribute returned by __getattribute__,
        # and it was either not saved in translatables or not listed in translatable_fields.
        raise AttributeError

    class Meta:
        abstract = True
