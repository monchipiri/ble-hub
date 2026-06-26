from app.actions.alert import AlertAction
from app.actions.log_activity import LogActivityAction
from app.actions.webhook import WebhookAction

ACTION_REGISTRY = {
    "alert": AlertAction(),
    "log_activity": LogActivityAction(),
    "database_log": LogActivityAction(),
    "webhook": WebhookAction(),
}
