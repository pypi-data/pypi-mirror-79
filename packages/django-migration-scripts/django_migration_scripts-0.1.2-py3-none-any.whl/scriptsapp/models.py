from django.db import models


class MigrationScripts(models.Model):
    app = models.CharField(max_length=255)
    migration_name = models.CharField(max_length=255)
    applied = models.BooleanField(default=False)
    applied_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)