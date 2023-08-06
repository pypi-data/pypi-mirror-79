from __future__ import absolute_import

import requests
from sentry import tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry_plugins.base import CorePluginMixin


class DingtalkPlugin(CorePluginMixin, notify.NotificationPlugin):
    title = "dingtalk"
    slug = "dingtalk"
    description = "Post notifications to a DingDing webhook."
    conf_key = "dingtalk"
    required_field = "webhook"
    feature_descriptions = [
        FeatureDescription(
            """
            Configure rule based dingding notifications to automatically be posted into a
            specific channel. Want any error that's happening more than 100 times a
            minute to be posted in `#critical-errors`? Setup a rule for it!
            """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    def is_configured(self, project):
        return bool(self.get_option("webhook", project))

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "Webhook URL",
                "type": "url",
                "placeholder": "https://oapi.dingtalk.com/robot/send?access_token=abcdefg",
                "required": True,
                "help": "Your custom dingding webhook URL.",
            },
            {
                "name": "custom_message",
                "label": "Custom Message",
                "type": "string",
                "placeholder": "e.g. Hey <!everyone> there is something wrong",
                "required": False,
                "help": "Optional - dingding message formatting can be used",
            },
            {
                "name": "include_tags",
                "label": "Include Tags",
                "type": "bool",
                "required": False,
                "help": "Include tags with notifications",
            },
            {
                "name": "included_tag_keys",
                "label": "Included Tags",
                "type": "string",
                "required": False,
                "help": (
                    "Only include these tags (comma separated list). " "Leave empty to include all."
                ),
            },
            {
                "name": "include_rules",
                "label": "Include Rules",
                "type": "bool",
                "required": False,
                "help": "Include triggering rules with notifications.",
            },
        ]

    def _get_tags(self, event):
        tag_list = event.tags
        if not tag_list:
            return ()

        return (
            (tagstore.get_tag_key_label(k), tagstore.get_tag_value_label(k, v)) for k, v in tag_list
        )

    def get_tag_list(self, name, project):
        option = self.get_option(name, project)
        if not option:
            return None
        return set(tag.strip().lower() for tag in option.split(","))

    def notify(self, notification, raise_exception=False):
        event = notification.event
        group = event.group
        project = group.project

        if not self.is_configured(project):
            return

        title = event.title.encode("utf-8")
        # TODO(dcramer): we'd like this to be the event culprit, but Sentry
        # does not currently retain it
        if group.culprit:
            culprit = group.culprit.encode("utf-8")
        else:
            culprit = None
        project_name = project.get_full_name().encode("utf-8")

        fields = []

        # They can be the same if there is no culprit
        # So we set culprit to an empty string instead of duplicating the text
        if culprit and title != culprit:
            fields.append(
                {"title": "Culprit", "value": culprit, "short": False})
        fields.append(
            {"title": "Project", "value": project_name, "short": True})

        if self.get_option("custom_message", project):
            fields.append(
                {
                    "title": "Custom message",
                    "value": self.get_option("custom_message", project),
                    "short": False,
                }
            )

        if self.get_option("include_rules", project):
            rules = []
            for rule in notification.rules:
                rule_link = "/%s/%s/settings/alerts/rules/%s/" % (
                    group.organization.slug,
                    project.slug,
                    rule.id,
                )

                # Make sure it's an absolute uri since we're sending this
                # outside of Sentry into Slack
                rule_link = absolute_uri(rule_link)
                rules.append((rule_link, rule.label))

            if rules:
                value = u", ".join(u"<{} | {}>".format(*r) for r in rules)

                fields.append(
                    {"title": "Triggered By", "value": value.encode(
                        "utf-8"), "short": False}
                )

        if self.get_option("include_tags", project):
            included_tags = set(self.get_tag_list(
                "included_tag_keys", project) or [])
            excluded_tags = set(self.get_tag_list(
                "excluded_tag_keys", project) or [])
            for tag_key, tag_value in self._get_tags(event):
                key = tag_key.lower()
                std_key = tagstore.get_standardized_key(key)
                if included_tags and key not in included_tags and std_key not in included_tags:
                    continue
                if excluded_tags and (key in excluded_tags or std_key in excluded_tags):
                    continue
                fields.append(
                    {
                        "title": tag_key.encode("utf-8"),
                        "value": tag_value.encode("utf-8"),
                        "short": True,
                    }
                )
        payload = {
            "attachments": [
                {
                    "fallback": "[%s] %s" % (project_name, title),
                    "title": title,
                    "title_link": group.get_absolute_url(params={"referrer": "slack"}),
                    "fields": fields,
                }
            ]
        }

        webhookUrl = self.get_option("webhook", project)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {"msgtype": "text",
                "text": {
                    "content": json.dumps(payload)
                }
                }
        requests.post(url, data=json.dumps(data), headers=headers)
