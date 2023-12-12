from django.db import models


class TestModel(models.Model):
    test_text = models.CharField(
        verbose_name="Test field",
        max_length=255,
    )
