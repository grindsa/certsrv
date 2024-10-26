import os
import time
from certsrv import Certsrv

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import sys


if __name__ == '__main__':


    # os.environ['KRB5_CONFIG'] = '/home/joern/krb5.conf'
    #host = 'WIN-4CLRCPMIM5E.bar.local'
    #user = 'joern'
    #password = 'Test1234'
    #template = 'WebSrv'
    #auth_method = 'gssapi'
    #ca_bundle = 'bar.local.pem'

    # host = 'ec2amaz-ui0qfbn.notademo.nclm.local'
    host = 'ec2-18-159-250-192.eu-central-1.compute.amazonaws.com'
    user = 'jmewes'
    password = 'Pass10@30@§34Pass1@3@§43'
    # template = 'WebSrv'
    template = 'WebServer'
    auth_method = 'ntlm'
    ca_bundle = 'ca_bundle.pem'


    uts_now = int(time.time())
    common_name = f'{uts_now}.myserver.bar.local'


    print(f'Common Name to set: {common_name}')
    # Generate a key
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    # key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    # Generate a CSR
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(common_name),
        ]),
        critical=False,
    ).sign(key, hashes.SHA256(), default_backend())

    # Get the cert from the ADCS server
    pem_req = csr.public_bytes(serialization.Encoding.PEM)
    print(pem_req)

    ca_server = Certsrv(host, username=user, password=password, auth_method=auth_method, cafile=ca_bundle)

    # check connection and credentials
    auth_check = ca_server.check_credentials()
    print(f'Auth check: {auth_check}')

    try:
        pem_cert = ca_server.get_cert(pem_req, template)
    except Exception as err:
        print(f'Error: {err}')
        sys.exit(1)
    cert = x509.load_pem_x509_certificate(pem_cert, default_backend())
    cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    print("Cert:\n{}".format(pem_cert.decode()))
    print(f'Common Name from cert: {cn}')
