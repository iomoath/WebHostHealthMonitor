from common_functions import *
import emsg_constructor
from config import *
import email_services
import slack_services
import requests
import http.client
import socket
import warnings
import urllib3

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def get_datetime():
    return datetime.now().strftime(DATETIME_FORMAT)


def build_event_info_dict(http_status_code, site_config, exception):


    message_subject = "{} | {} | {}".format(DEFAULT_URGENCY, site_config['name'], "Web Service Unreachable")
    url =  str(site_config.get('url'))

    new_dict = {'msg_subject': message_subject,
                'event_time': get_datetime(),
                'webhost_name': site_config.get('name'),
                #'URL': "{}".format(site_config.get('url')),
                'urgency': DEFAULT_URGENCY,
                'http_status_code': http_status_code,
                'exception': None,
                'exception_type': None}

    # Replace http, https with hxxps .. Original links are replaced by Outlook https://eur03.safelinks.protection.outlook.com/?.......
    url = url.replace("https://", "hxxps://")
    url = url.replace("http://", "hxxp://")
    new_dict['URL'] = url

    if exception is not None:
        new_dict['exception'] = str(exception)
        new_dict['exception_type'] = str(type(exception))

    return new_dict




def http_get(remote_host, proxy=None):
    headers = {'User-Agent': USER_AGENT,
               'Connection': 'Close',
               'Accept-Encoding': 'gzip, deflate',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'DNT': '1',
               'Upgrade-Insecure-Requests': '1',
               'Accept-Language': 'en-US,en;q=0.5'}

    url = remote_host.strip().rstrip('/')
    response = requests.get(url, headers=headers, verify=False, proxies=proxy, timeout=TIMEOUT)
    return response




def process_http_response(host_config, http_request_response, exception):
    if http_request_response is None or not http_request_response.headers:
        event_info = build_event_info_dict(0, host_config, exception)
    else:
        event_info = build_event_info_dict(http_request_response.status_code, host_config, exception)

    # Report
    report_event(event_info)



def check_hosts_reachability():
    # Read clients config from clients_confing.json
    client_configs = get_client_configs()

    current_index = 0
    for config in client_configs:
        try:
            web_site_name = config["name"]
            url = config["url"]
        except KeyError as e:
            print_verbose("[-] Error parsing #{} configuration. {}. Skipping.".format(current_index, e))
            continue


        if '' in (web_site_name, url):
            print_verbose("[-] Error in #{} configuration values. Skipping.".format(current_index))
            continue

        http_result=None
        try:

            print_verbose("\n[*] Connecting to '{}'".format(web_site_name))

            http_result = http_get(remote_host=url, proxy=None)


            response_code = http_result.status_code
            if response_code == 200:
                print_verbose("\n[+] Successfully connected to '{}'".format(web_site_name))
                continue

            # Connection issues..
            process_http_response(host_config=config, http_request_response=http_result, exception=None)

        except (requests.exceptions.ConnectTimeout, socket.timeout, urllib3.exceptions.MaxRetryError) as e:
            print_verbose("[-] ERROR: Connection to '{}' has timed out ___ {}".format(web_site_name, e))
            process_http_response(host_config=config, http_request_response=http_result, exception=e)
        except http.client.RemoteDisconnected as e:
            print_verbose("[-] ERROR: Connection closed by the remote host {} ___ {}".format(web_site_name, e))
            process_http_response(host_config=config, http_request_response=http_result, exception=e)
        except Exception as e:
            print_verbose("[-] ERROR: {} ___ {}".format(web_site_name, e))
            process_http_response(host_config=config, http_request_response=http_result, exception=e)




def construct_email_for_sending(msg_info_dict):
    try:
        attachments = decode_base64(msg_info_dict["attachments"])
    except:
        attachments = None

    dict_msg = {
        "use_smtp": USE_SMTP,
        "username": SMTP_USERNAME,
        "password": SMTP_PASSWORD,
        "host": SMTP_HOST,
        "port": SMTP_PORT,
        "ssl": SMTP_SSL,
        "from": "{} <{}>".format(FROM_NAME, FROM),
        "recipients": TO.split(','),
        "message": msg_info_dict["body"],
        "subject": msg_info_dict["subject"],
        "attachments": attachments}

    return dict_msg




def report_event(event_info):
    if SLACK_NOTIFICATIONS_ENABLED:
        print_verbose("[+] Pushing event details to Slack channel.")
        msg_dict = emsg_constructor.construct_email_notification_msg_dict(event_info)
        slack_services.send_message(msg_dict)

    if EMAIL_NOTIFICATIONS_ENABLED:
        print_verbose("[+] Sending event details by email")
        msg_dict = emsg_constructor.construct_email_notification_msg_dict(event_info)
        msg_dict_full = construct_email_for_sending(msg_dict)
        email_services.send_message(msg_dict_full)
