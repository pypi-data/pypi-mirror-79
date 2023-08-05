import asyncio
import difflib
import email.utils
import functools
import html
import itertools
import logging
import os
import re
import sys
import time

from markdown2 import Markdown

import requests

import webchanges as project
from .mailer import SMTPMailer, SendmailMailer
from .util import TrackSubClasses, chunkstring
from .xmpp import XMPP

try:
    import keyring
except ImportError:
    keyring = None

try:
    import chump
except ImportError:
    chump = None

try:
    import matrix_client.api
except ImportError:
    matrix_client = None

try:
    from pushbullet import Pushbullet
except ImportError:
    Pushbullet = None

logger = logging.getLogger(__name__)

# Regular expressions that match the added/removed markers of GNU wdiff output
WDIFF_ADDED_RE = r'[{][+].*?[+][}]'
WDIFF_REMOVED_RE = r'[\[][-].*?[-][]]'


class ReporterBase(object, metaclass=TrackSubClasses):
    __subclasses__ = {}

    def __init__(self, report, config, job_states, duration):
        self.report = report
        self.config = config
        self.job_states = job_states
        self.duration = duration

    def convert(self, othercls):
        if hasattr(othercls, '__kind__'):
            config = self.report.config['report'][othercls.__kind__]
        else:
            config = {}

        return othercls(self.report, config, self.job_states, self.duration)

    @classmethod
    def reporter_documentation(cls):
        result = []
        for sc in TrackSubClasses.sorted_by_kind(cls):
            result.extend((
                '  * %s - %s' % (sc.__kind__, sc.__doc__),
            ))
        return '\n'.join(result)

    @classmethod
    def submit_one(cls, name, report, job_states, duration):
        subclass = cls.__subclasses__[name]
        cfg = report.config['report'].get(name, {'enabled': False})
        if cfg['enabled']:
            subclass(report, cfg, job_states, duration).submit()
        else:
            raise ValueError(f'Reporter not enabled: {name}')

    @classmethod
    def submit_all(cls, report, job_states, duration):
        any_enabled = False
        for name, subclass in cls.__subclasses__.items():
            cfg = report.config['report'].get(name, {'enabled': False})
            if cfg['enabled']:
                any_enabled = True
                logger.info('Submitting with %s (%r)', name, subclass)
                subclass(report, cfg, job_states, duration).submit()

        if not any_enabled:
            logger.warning('No reporters enabled.')

    def submit(self):
        raise NotImplementedError()


class HtmlReporter(ReporterBase):
    def submit(self):
        yield from (str(part) for part in self._parts())

    def _parts(self):
        cfg = self.report.config['report']['html']

        yield """
            <!DOCTYPE html>
            <html>
            <head>
            <title>urlwatch</title>
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="font-family:Arial,Helvetica,sans-serif;font-size:13px;">"""

        for job_state in self.report.get_filtered_job_states(self.job_states):
            job = job_state.job

            if job.url:
                title = '<h2>{verb}: <a href="{location}">{pretty_name}</a></h2>'
            elif job.pretty_name() != job.get_location():
                title = '<h2>{verb}: <span title="{location}">{pretty_name}</span></h2>'
            else:
                title = '<h2>{verb}: {location}</h2>'

            yield title.format(verb=job_state.verb.title(),
                               location=html.escape(job.get_location()),
                               pretty_name=html.escape(job.pretty_name()))

            content = self._format_content(job_state, cfg['diff'])
            if content is not None:
                yield content

            yield '<hr>'

        duration = self.duration.seconds
        if duration < 10:
            duration += round(self.duration.microseconds / 1e6, 1)
        elif duration < 1:
            duration += round(self.duration.microseconds / 1e6, 2)
        yield (f"""
            <div style="font-style:italic">
            Watched {len(self.job_states)} URLs in {duration} seconds with <a href="{html.escape(project.__url__)}">
            {html.escape(project.__package__)}</a></address> {html.escape(project.__version__)}
            </div>
            </body>
            </html>""")

    def _diff_to_html(self, unified_diff, is_markdown=False):
        if is_markdown:
            # rebuild html from markdown using markdown2 library's Markdown
            markdowner = Markdown(safe_mode='escape', extras=['strike', 'target-blank-links'])
            atags = re.compile(r'<a ')
            htags = re.compile(r'<(/?)h\d>')
            tags = re.compile(r'^<p>(<code>)?|(</code>)?</p>$')

            def mark_to_html(text):
                """converts Markdown (as generated by pyhtml2text filter) back to html"""
                if text == '* * *':  # manually expand horizontal ruler since <hr> tag is used by us to separate jobs
                    return '-' * 80
                pre = ''
                if text.lstrip().startswith('* '):  # item of unordered list
                    lstripped = text.lstrip(' ')
                    indent = len(text) - len(lstripped)
                    pre = '&nbsp;' * indent
                    pre += '● ' if indent == 2 else '⯀ ' if indent == 4 else '○ '
                    text = text.split('* ', 1)[1]
                elif text.startswith(' '):  # replace leading spaces or converter will strip
                    lstripped = text.lstrip()
                    text = '&nbsp;' * (len(text) - len(lstripped)) + lstripped
                html_out = markdowner.convert(text).strip('\n')  # convert markdown to html
                html_out = atags.sub('<a style="font-family:inherit;color:inherit" ', html_out)  # fix <a> tag styling
                html_out, sub = tags.subn('', html_out)  # remove added tags
                if sub:
                    return pre + html_out
                html_out = htags.sub(r'<\g<1>strong>', html_out)  # replace heading tags with <strong>
                return pre + html_out

            yield '<span style="font-family:monospace">'
            for i, line in enumerate(unified_diff.splitlines()):
                pre = '</span>' if i == 2 else ''
                if line[0] == '+':
                    yield (f'{pre}<span style="color:green"><span style="font-family:monospace">+</span>'
                           f'{mark_to_html(line[1:])}</span><br>')
                elif line[0] == '-':
                    yield (f'{pre}<span style="color:red"><span style="font-family:monospace">-</span>'
                           f'{mark_to_html(line[1:])}</span><br>')
                elif line[0] == '@':
                    yield (f'{pre}<span style="background-color:whitesmoke;font-family:monospace">{html.escape(line)}'
                           f'</span><br>')
                else:
                    yield (f'{pre}<span style="font-family:monospace">{line[0].replace(" ", "&nbsp;")}</span>'
                           f'{mark_to_html(line[1:])}<br>')
            yield '\n'

        else:
            yield '<pre style="white-space:pre-wrap">'
            for line in unified_diff.splitlines():
                if line[0] == '+':
                    yield f'<span style="color:green">{html.escape(line)}</span>'
                elif line[0] == '-':
                    yield f'<span style="color:red">{html.escape(line)}</span>'
                elif line[0] == '@':
                    yield f'<span style="background-color:whitesmoke">{html.escape(line)}</span>'
                else:
                    yield html.escape(line)
            yield '</pre>\n'

    def _format_content(self, job_state, difftype):
        if job_state.verb == 'error':
            return f'<pre style="white-space:pre-wrap;color:red;">{html.escape(job_state.traceback.strip())}</pre>'

        if job_state.verb == 'unchanged':
            return f'<pre style="white-space:pre-wrap">{html.escape(job_state.old_data)}</pre>'

        if job_state.old_data in (None, job_state.new_data):
            return '...'

        if difftype == 'unified':
            # Style should include 'padding-left:2.3em;text-indent:-2.3em' to have hanging indents of long lines
            # but Gmail strips the 'text-indent:-2.3em' and end up with everything indented
            return '\n'.join(self._diff_to_html(job_state.get_diff(), job_state.job.is_markdown))

        elif difftype == 'table':
            timestamp_old = email.utils.formatdate(job_state.timestamp, localtime=True)
            timestamp_new = email.utils.formatdate(time.time(), localtime=True)
            html_diff = difflib.HtmlDiff()
            table = html_diff.make_table(job_state.old_data.splitlines(keepends=True),
                                         job_state.new_data.splitlines(keepends=True),
                                         timestamp_old, timestamp_new, True, 3)
            table = table.replace('<th ', '<th style="font-family:monospace" ')
            table = table.replace('<td ', '<td style="font-family:monospace" ')
            table = table.replace(' nowrap="nowrap"', '')
            table = table.replace('<a ', '<a style="font-family:monospace;color:inherit" ')
            table = table.replace('<span class="diff_add"', '<span style="color:green;background-color:lightgreen"')
            table = table.replace('<span class="diff_sub"', '<span style="color:red;background-color:lightred"')
            table = table.replace('<span class="diff_chg"', '<span style="color:orange;background-color:lightyellow"')
            return table
        else:
            raise ValueError('Diff style not supported: %r' % (difftype,))


class TextReporter(ReporterBase):
    def submit(self):
        cfg = self.report.config['report']['text']
        line_length = cfg['line_length']
        show_details = cfg['details']
        show_footer = cfg['footer']

        if cfg['minimal']:
            for job_state in self.report.get_filtered_job_states(self.job_states):
                pretty_name = job_state.job.pretty_name()
                location = job_state.job.get_location()
                if pretty_name != location:
                    location = '%s ( %s )' % (pretty_name, location)
                yield ': '.join((job_state.verb.upper(), location))
            return

        summary = []
        details = []
        for job_state in self.report.get_filtered_job_states(self.job_states):
            summary_part, details_part = self._format_output(job_state, line_length)
            summary.extend(summary_part)
            details.extend(details_part)

        if summary:
            sep = (line_length * '=') or None
            yield from (part for part in itertools.chain(
                (sep,),
                ('%02d. %s' % (idx + 1, line) for idx, line in enumerate(summary)),
                (sep, ''),
            ) if part is not None)

        if show_details:
            yield from details

        if summary and show_footer:
            yield from ('-- ',
                        '%s %s, %s' % (project.__project_name__, project.__version__, project.__copyright__),
                        'Website: %s' % (project.__url__,),
                        'watched %d URLs in %d seconds' % (len(self.job_states), self.duration.seconds))

    def _format_content(self, job_state):
        if job_state.verb == 'error':
            return job_state.traceback.strip()

        if job_state.verb == 'unchanged':
            return job_state.old_data

        if job_state.old_data in (None, job_state.new_data):
            return None

        return job_state.get_diff()

    def _format_output(self, job_state, line_length):
        summary_part = []
        details_part = []

        pretty_name = job_state.job.pretty_name()
        location = job_state.job.get_location()
        if pretty_name != location:
            location = '%s ( %s )' % (pretty_name, location)

        pretty_summary = ': '.join((job_state.verb.upper(), pretty_name))
        summary = ': '.join((job_state.verb.upper(), location))
        content = self._format_content(job_state)

        summary_part.append(pretty_summary)

        sep = (line_length * '-') or None
        details_part.extend((sep, summary, sep))
        if content is not None:
            details_part.extend((content, sep))
        details_part.extend(('', '') if sep else ('',))
        details_part = [part for part in details_part if part is not None]

        return summary_part, details_part


class StdoutReporter(TextReporter):
    """Print summary on stdout (the console)"""

    __kind__ = 'stdout'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_color = sys.stdout.isatty() and self.config.get('color', False)

    def _incolor(self, color_id, s):
        if self._has_color:
            return '\033[9%dm%s\033[0m' % (color_id, s)
        return s

    def _red(self, s):
        return self._incolor(1, s)

    def _green(self, s):
        return self._incolor(2, s)

    def _yellow(self, s):
        return self._incolor(3, s)

    def _blue(self, s):
        return self._incolor(4, s)

    def _get_print(self):
        if os.name == 'nt' and self._has_color:
            from colorama import AnsiToWin32
            return functools.partial(print, file=AnsiToWin32(sys.stdout).stream)
        return print

    def submit(self):
        print = self._get_print()

        cfg = self.report.config['report']['text']
        line_length = cfg['line_length']

        separators = (line_length * '=', line_length * '-', '-- ') if line_length else ()
        body = '\n'.join(super().submit())

        for line in body.splitlines():
            # Basic colorization for wdiff-style differences
            line = re.sub(WDIFF_ADDED_RE, lambda x: self._green(x.group(0)), line)
            line = re.sub(WDIFF_REMOVED_RE, lambda x: self._red(x.group(0)), line)

            # FIXME: This isn't ideal, but works for now...
            if line in separators:
                print(line)
            elif line.startswith('+'):
                print(self._green(line))
            elif line.startswith('-'):
                print(self._red(line))
            elif any(line.startswith(prefix) for prefix in ('NEW:', 'CHANGED:', 'UNCHANGED:', 'ERROR:')):
                first, second = line.split(' ', 1)
                if line.startswith('ERROR:'):
                    print(first, self._red(second))
                else:
                    print(first, self._blue(second))
            else:
                print(line)


class EMailReporter(TextReporter):
    """Send summary via e-mail (including SMTP)"""

    __kind__ = 'email'

    def submit(self):
        filtered_job_states = list(self.report.get_filtered_job_states(self.job_states))

        subject_args = {
            'count': len(filtered_job_states),
            'jobs': ', '.join(job_state.job.pretty_name() for job_state in filtered_job_states),
        }
        subject = self.config['subject'].format(**subject_args)

        body_text = '\n'.join(super().submit())

        if not body_text:
            logger.debug('Not sending e-mail (no changes)')
            return
        if self.config['method'] == "smtp":
            smtp_user = self.config['smtp'].get('user', None) or self.config['from']
            use_auth = self.config['smtp'].get('auth', False)
            mailer = SMTPMailer(smtp_user, self.config['smtp']['host'], self.config['smtp']['port'],
                                self.config['smtp']['starttls'], use_auth,
                                self.config['smtp'].get('insecure_password'))
        elif self.config['method'] == "sendmail":
            mailer = SendmailMailer(self.config['sendmail']['path'])
        else:
            logger.error(f'Invalid entry for method {self.config["method"]}')

        if self.config['html']:
            body_html = '\n'.join(self.convert(HtmlReporter).submit())

            msg = mailer.msg_html(self.config['from'], self.config['to'], subject, body_text, body_html)
        else:
            msg = mailer.msg_plain(self.config['from'], self.config['to'], subject, body_text)

        mailer.send(msg)


class IFTTTReport(TextReporter):
    """Send summary via IFTTT"""

    __kind__ = 'ifttt'

    def submit(self):
        webhook_url = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'.format(**self.config)
        for job_state in self.report.get_filtered_job_states(self.job_states):
            pretty_name = job_state.job.pretty_name()
            location = job_state.job.get_location()
            _ = requests.post(webhook_url, json={
                'value1': job_state.verb,
                'value2': pretty_name,
                'value3': location,
            })


class WebServiceReporter(TextReporter):
    MAX_LENGTH = 1024

    def web_service_get(self):
        raise NotImplementedError

    def web_service_submit(self, service, title, body):
        raise NotImplementedError

    def submit(self):
        body_text = '\n'.join(super().submit())

        if not body_text:
            logger.debug('Not sending %s (no changes)', self.__kind__)
            return

        if len(body_text) > self.MAX_LENGTH:
            body_text = body_text[:self.MAX_LENGTH]

        try:
            service = self.web_service_get()
        except Exception:
            logger.error('Failed to load or connect to %s - are the dependencies installed and configured?',
                         self.__kind__, exc_info=True)
            return

        self.web_service_submit(service, 'Website Change Detected', body_text)


class PushoverReport(WebServiceReporter):
    """Send summary via pushover.net"""

    __kind__ = 'pushover'

    def web_service_get(self):
        if chump is None:
            raise ImportError('Python module "chump" not installed')

        app = chump.Application(self.config['app'])
        return app.get_user(self.config['user'])

    def web_service_submit(self, service, title, body):
        sound = self.config['sound']
        # If device is the empty string or not specified at all, use None to send to all devices
        # (see https://github.com/thp/urlwatch/issues/372)
        device = self.config.get('device', None) or None
        priority = {
            'lowest': chump.LOWEST,
            'low': chump.LOW,
            'normal': chump.NORMAL,
            'high': chump.HIGH,
            'emergency': chump.EMERGENCY,
        }.get(self.config.get('priority', None), chump.NORMAL)
        msg = service.create_message(title=title, message=body, html=True, sound=sound, device=device,
                                     priority=priority)
        msg.send()


class PushbulletReport(WebServiceReporter):
    """Send summary via pushbullet.com"""

    __kind__ = 'pushbullet'

    def web_service_get(self):
        if Pushbullet is None:
            raise ImportError('Python module "pushbullet" not installed')

        return Pushbullet(self.config['api_key'])

    def web_service_submit(self, service, title, body):
        service.push_note(title, body)


class MailGunReporter(TextReporter):
    """Send e-mail via the Mailgun service"""

    __kind__ = 'mailgun'

    def submit(self):
        region = self.config.get('region', '')
        domain = self.config['domain']
        api_key = self.config['api_key']
        from_name = self.config['from_name']
        from_mail = self.config['from_mail']
        to = self.config['to']

        if region == 'us':
            region = ''

        if region != '':
            region = f'.{region}'

        filtered_job_states = list(self.report.get_filtered_job_states(self.job_states))
        subject_args = {
            'count': len(filtered_job_states),
            'jobs': ', '.join(job_state.job.pretty_name() for job_state in filtered_job_states),
        }
        subject = self.config['subject'].format(**subject_args)

        body_text = '\n'.join(super().submit())
        body_html = '\n'.join(self.convert(HtmlReporter).submit())

        if not body_text:
            logger.debug('Not calling Mailgun API (no changes)')
            return

        logger.debug(f"Sending Mailgun request for domain:'{domain}'")
        result = requests.post(
            f"https://api{region}.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={"from": f"{from_name} <{from_mail}>",
                  "to": to,
                  "subject": subject,
                  "text": body_text,
                  "html": body_html})

        try:
            json_res = result.json()

            if (result.status_code == requests.codes.ok):
                logger.info(f"Mailgun response: id '{json_res['id']}'. {json_res['message']}")
            else:
                logger.error(f"Mailgun error: {json_res['message']}")
        except ValueError:
            logger.error(
                f"Failed to parse Mailgun response. HTTP status code: {result.status_code}, content: {result.content}")

        return result


class TelegramReporter(TextReporter):
    """Send a message using Telegram"""
    MAX_LENGTH = 4096

    __kind__ = 'telegram'

    def submit(self):

        bot_token = self.config['bot_token']
        chat_ids = self.config['chat_id']
        chat_ids = [chat_ids] if isinstance(chat_ids, str) else chat_ids

        text = '\n'.join(super().submit())

        if not text:
            logger.debug('Not calling telegram API (no changes)')
            return

        result = None
        for chunk in chunkstring(text, self.MAX_LENGTH, numbering=True):
            for chat_id in chat_ids:
                res = self.submitToTelegram(bot_token, chat_id, chunk)
                if res.status_code != requests.codes.ok or res is None:
                    result = res

        return result

    def submitToTelegram(self, bot_token, chat_id, text):
        logger.debug(f"Sending telegram request to chat id:'{chat_id}'")
        result = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"})
        try:
            json_res = result.json()

            if (result.status_code == requests.codes.ok):
                logger.info(f"Telegram response: ok '{json_res['ok']}'. {json_res['result']}")
            else:
                logger.error(f"Telegram error: {json_res['description']}")
        except ValueError:
            logger.error(
                f"Failed to parse telegram response. HTTP status code: {result.status_code}, content: {result.content}")
        return result

    def chunkstring(self, string, length):
        return (string[0 + i:length + i] for i in range(0, len(string), length))


class SlackReporter(TextReporter):
    """Send a message to a Slack channel"""
    MAX_LENGTH = 40000

    __kind__ = 'slack'

    def submit(self):
        webhook_url = self.config['webhook_url']
        text = '\n'.join(super().submit())

        if not text:
            logger.debug('Not calling slack API (no changes)')
            return

        result = None
        for chunk in chunkstring(text, self.MAX_LENGTH, numbering=True):
            res = self.submit_to_slack(webhook_url, chunk)
            if res.status_code != requests.codes.ok or res is None:
                result = res

        return result

    def submit_to_slack(self, webhook_url, text):
        logger.debug(f"Sending slack request with text:{text}")
        post_data = {"text": text}
        result = requests.post(webhook_url, json=post_data)
        try:
            if result.status_code == requests.codes.ok:
                logger.info("Slack response: ok")
            else:
                logger.error(f"Slack error: {result.text}")
        except ValueError:
            logger.error(
                f"Failed to parse slack response. HTTP status code: {result.status_code}, content: {result.content}")
        return result


class MarkdownReporter(ReporterBase):
    def submit(self):
        cfg = self.report.config['report']['markdown']
        show_details = cfg['details']
        show_footer = cfg['footer']

        if cfg['minimal']:
            for job_state in self.report.get_filtered_job_states(self.job_states):
                pretty_name = job_state.job.pretty_name()
                location = job_state.job.get_location()
                if pretty_name != location:
                    location = '%s (%s)' % (pretty_name, location)
                yield '* ' + ': '.join((job_state.verb.upper(), location))
            return

        summary = []
        details = []
        for job_state in self.report.get_filtered_job_states(self.job_states):
            summary_part, details_part = self._format_output(job_state)
            summary.extend(summary_part)
            details.extend(details_part)

        if summary:
            yield from ('%d. %s' % (idx + 1, line) for idx, line in enumerate(summary))
            yield ''

        if show_details:
            yield from details

        if summary and show_footer:
            yield from ('--- ',
                        '%s %s, %s  ' % (urlwatch.project_name, urlwatch.__version__, urlwatch.__copyright__),
                        'Website: %s  ' % (urlwatch.__url__,),
                        'watched %d URLs in %d seconds' % (len(self.job_states), self.duration.seconds))

    def _format_content(self, job_state):
        if job_state.verb == 'error':
            return job_state.traceback.strip()

        if job_state.verb == 'unchanged':
            return job_state.old_data

        if job_state.old_data in (None, job_state.new_data):
            return None

        return job_state.get_diff()

    def _format_output(self, job_state):
        summary_part = []
        details_part = []

        pretty_name = job_state.job.pretty_name()
        location = job_state.job.get_location()
        if pretty_name != location:
            location = '%s (%s)' % (pretty_name, location)

        pretty_summary = ': '.join((job_state.verb.upper(), pretty_name))
        summary = ': '.join((job_state.verb.upper(), location))
        content = self._format_content(job_state)

        summary_part.append(pretty_summary)

        details_part.append('### ' + summary)
        if content is not None:
            details_part.extend(('', '```', content, '```', ''))
        details_part.extend(('', ''))

        return summary_part, details_part


class MatrixReporter(MarkdownReporter):
    """Send a message to a room using the Matrix protocol"""
    MAX_LENGTH = 4096

    __kind__ = 'matrix'

    def submit(self):
        if matrix_client is None:
            raise ImportError('Python module "matrix_client" not installed')

        homeserver_url = self.config['homeserver']
        access_token = self.config['access_token']
        room_id = self.config['room_id']

        body_markdown = '\n'.join(super().submit())

        if not body_markdown:
            logger.debug('Not calling Matrix API (no changes)')
            return

        if len(body_markdown) > self.MAX_LENGTH:
            body_markdown = body_markdown[:self.MAX_LENGTH]

        client_api = matrix_client.api.MatrixHttpApi(homeserver_url, access_token)

        body_html = Markdown().convert(body_markdown)

        client_api.send_message_event(
            room_id,
            "m.room.message",
            content={
                "msgtype": "m.text",
                "format": "org.matrix.custom.html",
                "body": body_markdown,
                "formatted_body": body_html
            }
        )


class XMPPReporter(TextReporter):
    """Send a message using the XMPP Protocol"""
    MAX_LENGTH = 262144

    __kind__ = 'xmpp'

    def submit(self):

        sender = self.config['sender']
        recipient = self.config['recipient']

        text = '\n'.join(super().submit())

        if not text:
            logger.debug('Not sending XMPP message (no changes)')
            return

        xmpp = XMPP(sender, recipient, self.config.get('insecure_password'))

        for chunk in chunkstring(text, self.MAX_LENGTH, numbering=True):
            asyncio.run(xmpp.send(chunk))


class BrowserReporter(HtmlReporter):
    """Display summary on the default web browser"""

    __kind__ = 'browser'

    def submit(self):
        filtered_job_states = list(self.report.get_filtered_job_states(self.job_states))

        if not filtered_job_states:
            logger.debug('Not opening browser (no changes)')
            return

        subject_args = {
            'count': len(filtered_job_states),
            'jobs': ', '.join(job_state.job.pretty_name() for job_state in filtered_job_states),
        }

        body_html = '\n'.join(self.convert(HtmlReporter).submit())
        title = self.config['title'].format(**subject_args)
        body_html = body_html.replace('</title>', f' {title}</title>')
        import tempfile
        import webbrowser
        import os

        f = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
        f.write(body_html)
        f.close()
        webbrowser.open(f.name)
        time.sleep(1)
        os.remove(f.name)
