# This import syntax is for python2!!!!!
from urllib2 import urlopen, Request
import re
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ConfigParser
import telnetlib

# Read the ini file
config = ConfigParser.ConfigParser()
config.sections()
config.read('/home/teamspeak/version_check/config.ini')

def fetch_content(domain):
    story = urlopen(Request(domain, headers={'User-Agent': 'Mozilla/5.0'}))
    content_lines = []
    for line in story:
        line_words = line.decode("utf-8").split()
        for word in line_words:
            content_lines.append(word)
    return content_lines

def extract_versions(lines):
    versions = []
    html_string = ''.join((lines)).encode('utf-8')
    version = re.search(r'(Server64-bit<spanclass="version">)([\d\.]{1,})', html_string)
    version = str(version.group(2))
    return version

def import_current_version():
    current_version = ''
    tn = telnetlib.Telnet(config.get('TSserver', 'ip'), config.get('TSserver', 'query_port'), 5)
    tn.read_until("command.\n".encode('ascii'))
    tn.write("version\n".encode('ascii'))
    current_version = tn.read_until("error id=0 msg=ok".encode('ascii'))
    current_version = re.search(r'(version=)([\d|\.]{1,}) ', str(current_version))
    current_version = current_version.group(2)
    return current_version

def compare_versions(new_version, current_version):
    if str(new_version) == str(current_version):
        print('Server is running on latest version')
    else:
        print('Server needs an update')
        hostname = socket.getfqdn()

        msg = MIMEMultipart()
        msg['From'] = config.get('MAIL', 'from_addr')
        msg['To'] = config.get('MAIL', 'to_addr')
        msg['Subject'] = "TeamSpeak server update available"
        body = '''
            Hello!
            your server ''' + hostname + ''' is currently running on version ''' + current_version + '''.
            The latest version is ''' + new_version + '''.

            Please consider an update. You can do this by running the corresponding .yml from this repository:
            https://github.com/siw36/ansible-teamspeak
        '''
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(config.get('MAIL', 'server'), config.get('MAIL', 'smtp_port'))
        server.starttls()
        server.login(config.get('MAIL', 'from_addr'), config.get('MAIL', 'password'))
        text = msg.as_string()
        server.sendmail(config.get('MAIL', 'from_addr'), config.get('MAIL', 'to_addr'), text)
        server.quit()

def main():
    domain = 'https://teamspeak.com/en/downloads/index.html#server'
    content = fetch_content(domain)
    version = extract_versions(content)
    current_version = import_current_version()
    compare_versions(version, current_version)

if __name__ == '__main__':
    main()
