################ Email Notifications settings ################
EMAIL_NOTIFICATIONS_ENABLED = True
USE_SMTP = False

SMTP_HOST = "smtp.example.net"
SMTP_PORT = 587
SMTP_USERNAME = "soc@example.org"
SMTP_PASSWORD = "123456"
SMTP_SSL = True


FROM = "web-monitor-agent@example.org"
FROM_NAME = "Web Monitor Agent"
TO = "soc@example.org"


################ Slack Notifications settings ################
SLACK_NOTIFICATIONS_ENABLED = False
SLACK_API_TOKEN = ''


################ General settings ################
CLIENT_CONFIGS_FILE = "hosts.json"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
TIMEOUT = 10

# Used to construct notifications. email, slack.
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# Default event urgency, TODO: set by http response code, connection time out..
DEFAULT_URGENCY = "CRITICAL"
################ Internal Global variables - values will be overridden  ################
VERBOSE_ENABLED = True
