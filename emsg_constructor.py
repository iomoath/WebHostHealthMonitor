def construct_email_notification_msg_dict(event_info_dict):

    # Message subject
    message_subject = event_info_dict['msg_subject']

    # Message body
    message_body = '{}{}'.format(message_subject, '\n\n')
    message_body += "Event Time: {}\n\n".format(event_info_dict['event_time'])

    message_body += "Website name: {}\n".format(event_info_dict['webhost_name'])
    message_body += "URL: {}\n".format(event_info_dict['URL'])
    message_body += "Urgency: {}\n".format(event_info_dict['urgency'])

    message_body += "HTTP Response Code: {}\n".format(event_info_dict['http_status_code'])
    message_body += "Exception Type: {}\n\n".format(event_info_dict['exception_type'])
    message_body += "Exception: {}\n".format(event_info_dict['exception'])
    msg_dict = {"subject": message_subject, "body": message_body, "attachment": None}
    return msg_dict


def construct_slack_notification_msg_dict(event_info_dict, slack_channel):

    # Message subject
    message_subject = event_info_dict['msg_subject']

    # Message body
    message_body = '*{}*{}'.format(message_subject, '\n\n')
    message_body += "Event Time: {}\n".format(event_info_dict['event_time'])

    message_body += "Host: {}\n".format(event_info_dict['host_name'])
    message_body += "URL: {}\n".format(event_info_dict['URL'])
    message_body += "Urgency: {}\n".format(event_info_dict['urgency'])

    message_body += "HTTP Response Code: {}\n".format(event_info_dict['http_code'])
    message_body += "Exception Type: {}\n".format(event_info_dict['exception_type'])
    message_body += "Exception: {}\n".format(event_info_dict['exception'])

    message_body += '_' * 50
    message_body += '\n'
    msg_dict = {"channel_name": slack_channel, "subject": message_subject, "body": message_body, "attachment": None}
    return msg_dict
