'''
Callback's and handlers for essential
EST URL's.
'''
from http.server import BaseHTTPRequestHandler
import os
import subprocess
import uuid


KEY = None  # pylint: disable=W0603


class EstRequestHandler(BaseHTTPRequestHandler):

    """HTTP Request hedler for EST essential messages """

    def do_GET(self):  # pylint: disable=C0103
        """"Implement essential EST HTTP GET messages."""

        path = self.path

        if path == '/.well-known/est/cacerts':
            self.handle_cacert()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def do_POST(self):  # pylint: disable=C0103
        """Implement Essential EST HTTP POST requests.
           Authenticate requests.
        """
        path = self.path
        if self.auth_isok():
            if path == '/.well-known/est/simpleenroll':
                self.handle_simpleenroll()
            elif path == '/.well-known/est/simplereenroll':
                self.handle_simplerenroll()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
        else:
            self.send_response(401)
            self.send_header('WWW-Authenticate',
                             'Basic  realm="paswd required" charset="UTF-8"')
            self.end_headers()

    def auth_isok(self):
        """Check if Authentication is required and ok.
           In case username and password are
           not set => Authentication is allways ok

        Returns:
            True if ok False if not.
        """
        # pylint: disable=W0603
        global KEY
        return_value = False
        if KEY is None:
            return_value = True
        elif self.headers.get('Authorization') == 'Basic ' + KEY:
            return_value = True
        return return_value

    def handle_cacert(self):
        """Handle cacert request.
           Read cacert from disk,create and send response.
        """

        file = open("./certs/cacert.p7b", "r")
        ca_certs = file.read()

        self.set_est_rsp_header(len(ca_certs))

        self.wfile.write(ca_certs.encode('utf-8'))

    def handle_simpleenroll(self):
        """Handler for simpleenroll request.
           Read request, create certificate and response.
        """
        content_length = int(self.headers['Content-Length'])
        csr = self.rfile.read(content_length)

        cert = sign_certificate(csr)

        self.set_est_rsp_header(len(cert))

        self.wfile.write(cert.encode('utf-8'))

    def handle_simplerenroll(self):
        """Basically indetical request-> handle with same handler."""
        self.handle_simpleenroll()

    def set_est_rsp_header(self, data_len):
        """ Utility to create rsp header for messages."""
        self.send_response(200)
        self.send_header('Content-type', 'application/pkcs7-mime')
        self.send_header('Content-Transfer-Encoding', 'base64')
        self.send_header('Content-Length', data_len)
        self.end_headers()


def sign_certificate(csr):
    """Create signed certificate.
       Stores request with unique name,
        call's signing script and remove created files.
        Args:
            csr certificate signing request.

        Returns:
            Signed certificate in base64 encoded format.
    """
    unique_filename = str(uuid.uuid4().hex)

    file = open("./csr_req/%s.csr" % unique_filename, "w")
    file.write(csr.decode("utf-8"))
    file.close()

    subprocess.run(["../ca/scripts/sign.sh", unique_filename], check=False)

    file = open("./csr_req/%s.p7b" % unique_filename, "r")
    cert = file.read()

    os.remove("./csr_req/%s.csr" % unique_filename)
    os.remove("./csr_req/%s.p7b" % unique_filename)

    return cert
