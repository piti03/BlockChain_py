#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from flask import Flask, request, make_response, Blueprint
from json import dumps, loads
from requests import post
from sys import exit, stderr
from os import symlink, readlink
from os.path import join, islink


def parse_args():
    epilog = None

    parser = ArgumentParser(description='A Flask app to republish to Slack',
                            epilog=epilog,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--host',
                        default='127.0.0.1',
                        help='listen host')
    parser.add_argument('-p', '--port',
                        default=8080,
                        type=int,
                        help='listen port')
    parser.add_argument('--install-service',
                        choices=['upstart'],
                        help='install service wrapper')
    parser.add_argument('--install-nginx-config',
                        action='store_true',
                        help='install nginx configs')
    parser.add_argument('--url',
                        help='public-facing url')
    parser.add_argument('--private-key',
                        help='SSL private key file')
    parser.add_argument('--certificate',
                        help='SSL certificate file')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Flask debug mode')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='print verbose output')
    args = parser.parse_args()

    return (args._get_args(), dict(args._get_kwargs()))


def _post_message(token, text, channel='#general', username='Slask', payload={}):
    payload.update({'token': token,
                    'channel': channel,
                    'text': text,
                    'username': username})
    return post("https://slack.com/api/chat.postMessage", params=payload)


blueprint = Blueprint('slask_blueprint', __name__)

@blueprint.route("/slask/<token>", methods=['POST'])
def _handle_one(token):
    r = _post_message(token, request.get_data())
    return make_response(r.text, r.status_code)

@blueprint.route("/slask/<token>/<channel>", methods=['POST'])
def _handle_two(token, channel):
    r = _post_message(token, request.get_data(), channel)
    return make_response(r.text, r.status_code)

@blueprint.route("/slask/<token>/<channel>/<username>", methods=['POST'])
def _handle_three(token, channel, username):
    r = _post_message(token, request.get_data(), channel, username)
    return make_response(r.text, r.status_code)

@blueprint.route("/slask/<token>/<channel>/<username>/<options>", methods=['POST'])
def _handle_four(token, channel, username, options):
    if options.lower().startswith("0x"):
        options = int(options, 16)
    elif options.startswith("0"):
        options = int(options, 8)
    else:
        options = int(options)

    text = request.get_data()
    if options & (1 << 1):
        try:
            text = dumps(loads(text), indent=4)
        except:
            pass
    if options & (1 << 0):
        text = '```%s```' % text

    payload = {}
    payload['link_names'] = 1 if options & (1 << 2) else 0

    r = _post_message(token, text, channel, username, payload)
    return make_response(r.text, r.status_code)


class slask():
    def __init__(self, *args, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

        if self.install_service is not None:
            self._install_service()

        if self.install_nginx_config:
            self._install_nginx_config()

        if self.install_service is not None or self.install_nginx_config:
            exit(0)

        self.app = Flask(__name__)
        self.app.register_blueprint(blueprint)


    def _install_service(self):
        script = None
        location = None
        if self.install_service == 'upstart':
            script = '''\
description "Slask"

start on runlevel [2345]
stop on runlevel [016]

respawn
respawn limit 10 5

exec slask %s''' % ' '.join(['--%s %s' % (kwarg, getattr(self, kwarg))
                             for kwarg in dir(self)
                             if kwarg in ['host', 'port']])
            location = '/etc/init/slask.conf'
        else:
            raise RuntimeError('Invalid service type')
    
        with open(location, 'w') as f:
            f.write(script)


    def _install_nginx_config(self):
        if self.url is None or self.private_key is None or self.certificate is None:
            raise RuntimeError('Must specify --url, --private-key, and --certificate')

        local_url = "%s:%s" % ('localhost' if self.host == '0.0.0.0' else self.host, self.port)
        config = '''\
server {
    listen              443 ssl;
    server_name         %s;
    ssl_certificate     %s;
    ssl_certificate_key %s;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    location / {
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;
  
        proxy_pass          http://%s;
        proxy_read_timeout  90;
  
        proxy_redirect      http://%s https://%s;
    }
}''' % (self.url, self.certificate, self.private_key, local_url, local_url, self.url)

        nginx_dir = '/etc/nginx'
        location = join(nginx_dir, 'sites-available', 'slask')
        link = join(nginx_dir, 'sites-enabled', 'slask')
        with open(location, 'w') as f:
            f.write(config)
        try:
            symlink(location, link)
        except OSError as e:
            if islink(link) and readlink(link) == location:
                pass
            else:
                raise e

    def run(self):
        context = None
#        if self.private_key is not None and self.certificate is not None:
#            import ssl
#            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
#            context.load_cert_chain(self.certificate, self.private_key)

        self.app.run(host=self.host, port=self.port, debug=self.debug, ssl_context=context)
