'''
Simple EST test server.
'''
from http.server import HTTPServer
import ssl
import base64
import argparse
import estrequest as est


def run_server(args):
    ''' Initilize and run server.
    '''
    cert_mode = [ssl.CERT_NONE, ssl.CERT_OPTIONAL, ssl.CERT_REQUIRED]
    purpose = ssl.Purpose.CLIENT_AUTH

    context = ssl.create_default_context(purpose, cafile=args.cafile)
    context.verify_mode = cert_mode[args.certmode]
    context.load_cert_chain(keyfile=args.key, certfile=args.cert)

    httpd = HTTPServer(('0.0.0.0', args.port), est.EstRequestHandler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()


def handle_args(parser):
    '''Handle commandline arguments.
    '''
    parser.add_argument("-p", "--port", type=int,
                        help="Server port", required=True)

    parser.add_argument("-u", "--user", default=None,
                        help="Login crendentials username:password")

    parser.add_argument("-ca", "--cafile", default="./certs/cacert.pem",
                        help="Ca certificate")

    parser.add_argument("-c", "--cert", default="./certs/servercert.pem",
                        help="server certificate")

    parser.add_argument("-k", "--key", default="./certs/serverkey.pem",
                        help="Certificate private key")

    parser.add_argument("-cm", "--certmode", default=1,
                        type=int, choices=[0, 1, 2],
                        help="Certicate mode 0=CERT_NONE 1=CERT_OPTIONAL 2=CERT_REQUIRED")

    return parser.parse_args()


if __name__ == '__main__':
    ARGS = handle_args(argparse.ArgumentParser())

    if ARGS.user is not None:
        est.KEY = base64.b64encode(ARGS.user.encode('utf-8')).decode("utf-8")

    run_server(ARGS)
