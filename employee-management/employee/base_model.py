# employee/models/base_model.py

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that includes created_at and updated_at fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when this record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date and time when this record was last updated."
    )

    class Meta:
        abstract = True
