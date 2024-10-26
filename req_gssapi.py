#!/usr/bin/python3
import os
import requests
import gssapi
# from requests_kerberos import HTTPKerberosAuth, REQUIRED, OPTIONAL, DISABLED
import requests_gssapi
# kinit
# curl --negotiate -u: 'http://win-4clrcpmim5e.bar.local/certsrv/'



if __name__ == '__main__':

    proto = 'http'
    hostname = 'win-4clrcpmim5e.bar.local'
    path = 'certsrv'
    # username = 'joern@BAR.LOCAL'
    username = 'joern'
    password = 'Test1234'
    oid = '1.3.6.1.5.5.2' # SPNEGO
    # oid = '1.2.840.113554.1.2.2' # krb5 default

    # os.environ['KRB5_CONFIG'] = '/home/joern/krb5.conf'

    cred = gssapi.raw.acquire_cred_with_password(
        gssapi.Name(username, gssapi.NameType.user),
        password.encode("utf-8"),
        mechs=[gssapi.OID.from_int_seq(oid)],
        usage="initiate",
    )

    session = requests.Session()
    session.auth = requests_gssapi.HTTPSPNEGOAuth(creds=cred.creds)
    # session.auth = requests_gssapi.HTTPSPNEGOAuth()
    response = session.get(f'{proto}://{hostname}/{path}/')
    print(response.status_code)

    response = session.get(f'{proto}://{hostname}/{path}/')
    print(response.status_code)

    response = session.get(f'{proto}://{hostname}/{path}/')
    print(response.status_code)

    # kerberos_auth = requests_gssapi.HTTPSPNEGOAuth(creds=cred.creds)
    # response = requests.get(f'{proto}://{hostname}/{path}/', auth=kerberos_auth)
    # print(response.status_code)
    # print('end')