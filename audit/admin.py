from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# The domain models are registered by their own app admin modules (for example,
# accounts/admin.py). Re-registering them here raises AlreadyRegistered during
# Django startup and prevents management commands and Docker builds from running.
# Keep this module intentionally empty; Simple History remains enabled through
# the model mixins/configuration used by the application.
