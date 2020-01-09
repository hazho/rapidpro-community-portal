from rapidpro_community_portal.settings.staging import *  # noqa

# There should be only minor differences from staging

DATABASES['default']['NAME'] = os.environ.get('DB_NAME', 'rapidpro_community_portal_production')  # noqa
DATABASES['default']['USER'] = os.environ.get('DB_USER', 'rapidpro_community_portal_production')  # noqa

EMAIL_SUBJECT_PREFIX = '[Rapidpro_Community_Portal Prod] '

# Used by Wagtail in sending emails for moderation
BASE_URL = 'https://community.rapidpro.io'

# Uncomment if using celery worker configuration
# BROKER_URL = 'amqp://rapidpro_community_portal_production:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/rapidpro_community_portal_production' % os.environ  # noqa
