import sentry_opsgenie
from sentry_opsgenie.forms import OpsGenieConfigForm
from sentry.plugins import Plugin

import sys
import urllib2
import json


class OpsGeniePlugin(Plugin):
    """
    Sentry plugin to send errors stats to OpsGenie.
    """
    author = 'William Hommel'
    author_url = 'https://github.com/whommel/sentry-opsgenie'
    version = sentry_opsgenie.VERSION
    description = 'Send error occurence to OpsGenie.'
    slug = 'opsgenie'
    title = 'OpsGenie'
    conf_key = slug
    conf_title = title
    resource_links = [
        ('Source', 'https://github.com/whommel/sentry-opsgenie'),
        ('Bug Tracker', 'https://github.com/whommel/sentry-opsgenie/issues'),
        ('README', 'https://github.com/whommel/sentry-opsgenie/blob/master/README.rst'),
    ]
    project_conf_form = OpsGenieConfigForm

    def is_configured(self, project, **kwargs):
        params = self.get_option
        return (params('api_key', project) and
                params('recipients', project) and
                params('alert_url', project))
                
    def post_process(self, group, event, is_new, is_sample, **kwargs):
        if not self.is_configured(group.project):
            return

        api_key = self.get_option('api_key', group.project)
        recipients = self.get_option('recipients', group.project)
        alert_url = self.get_option('alert_url', group.project)

        details = {
            'id': str(group.id),
            'checksum': group.checksum,
            'project': group.project.slug,
            'project_name': group.project.name,
            'logger': group.logger,
            'level': group.get_level_display(),
            'culprit': group.culprit,
            'url': group.get_absolute_url(),
            'server_name': event.server_name
        }

         details['event'] = dict(event.data or {})
        
        # populate the map that contains alert properties
        alertProps = {
           "apiKey":api_key,
           "message":event.message,
           "recipients":recipients,
           "source":"Sentry",
           "details":details
        }

        jdata = json.dumps(alertProps)
        response = urllib2.urlopen(alert_url, jdata)
        raw_response_data = response.read()
        response_data = json.loads(raw_response_data)
        if 'status' not in response_data:
            logger = logging.getLogger('sentry.plugins.opsgenie')
            logger.error('Unexpected response')
        if response_data['status'] != 'successful':
            logger = logging.getLogger('sentry.plugins.opsgenie')
            logger.error('Event was not sent to opsgenie')