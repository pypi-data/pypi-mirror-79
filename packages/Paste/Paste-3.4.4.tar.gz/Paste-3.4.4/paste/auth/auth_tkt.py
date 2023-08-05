# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
##########################################################################
#
# Copyright (c) 2005 Imaginary Landscape LLC and Contributors.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##########################################################################
"""
Implementation of cookie signing as done in `mod_auth_tkt
<http://www.openfusion.com.au/labs/mod_auth_tkt/>`_.

mod_auth_tkt is an Apache module that looks for these signed cookies
and sets ``REMOTE_USER``, ``REMOTE_USER_TOKENS`` (a comma-separated
list of groups) and ``REMOTE_USER_DATA`` (arbitrary string data).

This module is an alternative to the ``paste.auth.cookie`` module;
it's primary benefit is compatibility with mod_auth_tkt, which in turn
makes it possible to use the same authentication process with
non-Python code run under Apache.
"""
import six
import time as time_mod
try:
    import hashlib
except ImportError:
    # mimic hashlib (will work for md5, fail for secure hashes)
    import md5 as hashlib
try:
    from http.cookies import SimpleCookie
except ImportError:
    # Python 2
    from Cookie import SimpleCookie
from paste import request

try:
    from urllib import quote as url_quote # Python 2.X
    from urllib import unquote as url_unquote
except ImportError:
    from urllib.parse import quote as url_quote  # Python 3+
    from urllib.parse import unquote as url_unquote

DEFAULT_DIGEST = hashlib.md5


class AuthTicket(object):

    """
    This class represents an authentication token.  You must pass in
    the shared secret, the userid, and the IP address.  Optionally you
    can include tokens (a list of strings, representing role names),
    'user_data', which is arbitrary data available for your own use in
    later scripts.  Lastly, you can override the timestamp, cookie name,
    whether to secure the cookie and the digest algorithm (for details
    look at ``AuthTKTMiddleware``).

    Once you provide all the arguments, use .cookie_value() to
    generate the appropriate authentication ticket.  .cookie()
    generates a Cookie object, the str() of which is the complete
    cookie header to be sent.

    CGI usage::

        token = auth_tkt.AuthTick('sharedsecret', 'username',
            os.environ['REMOTE_ADDR'], tokens=['admin'])
        print('Status: 200 OK')
        print('Content-type: text/html')
        print(token.cookie())
        print("")
        ... redirect HTML ...

    Webware usage::

        token = auth_tkt.AuthTick('sharedsecret', 'username',
            self.request().environ()['REMOTE_ADDR'], tokens=['admin'])
        self.response().setCookie('auth_tkt', token.cookie_value())

    Be careful not to do an HTTP redirect after login; use meta
    refresh or Javascript -- some browsers have bugs where cookies
    aren't saved when set on a redirect.
    """

    def __init__(self, secret, userid, ip, tokens=(), user_data='',
                 time=None, cookie_name='auth_tkt',
                 secure=False, digest_algo=DEFAULT_DIGEST):
        self.secret = secret
        self.userid = userid
        self.ip = ip
        if not isinstance(tokens, six.string_types):
            tokens = ','.join(tokens)
        self.tokens = tokens
        self.user_data = user_data
        if time is None:
            self.time = time_mod.time()
        else:
            self.time = time
        self.cookie_name = cookie_name
        self.secure = secure
        if isinstance(digest_algo, six.binary_type):
            # correct specification of digest from hashlib or fail
            self.digest_algo = getattr(hashlib, digest_algo)
        else:
            self.digest_algo = digest_algo

    def digest(self):
        return calculate_digest(
            self.ip, self.time, self.secret, self.userid, self.tokens,
            self.user_data, self.digest_algo)

    def cookie_value(self):
        v = b'%s%08x%s!' % (self.digest(), int(self.time), maybe_encode(url_quote(self.userid)))
        if self.tokens:
            v += maybe_encode(self.tokens) + b'!'
        v += maybe_encode(self.user_data)
        return v

    def cookie(self):
        c = SimpleCookie()
        if six.PY3:
            import base64
            cookie_value = base64.b64encode(self.cookie_value())
        else:
            cookie_value = self.cookie_value().encode('base64').strip().replace('\n', '')
        c[self.cookie_name] = cookie_value
        c[self.cookie_name]['path'] = '/'
        if self.secure:
            c[self.cookie_name]['secure'] = 'true'
        return c


class BadTicket(Exception):
    """
    Exception raised when a ticket can't be parsed.  If we get
    far enough to determine what the expected digest should have
    been, expected is set.  This should not be shown by default,
    but can be useful for debugging.
    """
    def __init__(self, msg, expected=None):
        self.expected = expected
        Exception.__init__(self, msg)


def parse_ticket(secret, ticket, ip, digest_algo=DEFAULT_DIGEST):
    """
    Parse the ticket, returning (timestamp, userid, tokens, user_data).

    If the ticket cannot be parsed, ``BadTicket`` will be raised with
    an explanation.
    """
    if isinstance(digest_algo, six.binary_type):
        # correct specification of digest from hashlib or fail
        digest_algo = getattr(hashlib, digest_algo)
    digest_hexa_size = digest_algo().digest_size * 2
    ticket = ticket.strip(b'"')
    digest = ticket[:digest_hexa_size]
    try:
        timestamp = int(ticket[digest_hexa_size:digest_hexa_size + 8], 16)
    except ValueError as e:
        raise BadTicket('Timestamp is not a hex integer: %s' % e)
    try:
        userid, data = ticket[digest_hexa_size + 8:].split(b'!', 1)
    except ValueError:
        raise BadTicket('userid is not followed by !')
    userid = url_unquote(userid.decode())
    if b'!' in data:
        tokens, user_data = data.split(b'!', 1)
    else:
        # @@: Is this the right order?
        tokens = b''
        user_data = data

    expected = calculate_digest(ip, timestamp, secret,
                                userid, tokens, user_data,
                                digest_algo)

    if expected != digest:
        raise BadTicket('Digest signature is not correct',
                        expected=(expected, digest))

    tokens = tokens.split(b',')

    return (timestamp, userid, tokens, user_data)


# @@: Digest object constructor compatible with named ones in hashlib only
def calculate_digest(ip, timestamp, secret, userid, tokens, user_data,
                     digest_algo):
    secret = maybe_encode(secret)
    userid = maybe_encode(userid)
    tokens = maybe_encode(tokens)
    user_data = maybe_encode(user_data)
    digest0 = maybe_encode(digest_algo(
        encode_ip_timestamp(ip, timestamp) + secret + userid + b'\0'
        + tokens + b'\0' + user_data).hexdigest())
    digest = digest_algo(digest0 + secret).hexdigest()
    return maybe_encode(digest)


def encode_ip_timestamp(ip, timestamp):
    ip_chars = b''.join(map(six.int2byte, map(int, ip.split('.'))))
    t = int(timestamp)
    ts = ((t & 0xff000000) >> 24,
          (t & 0xff0000) >> 16,
          (t & 0xff00) >> 8,
          t & 0xff)
    ts_chars = b''.join(map(six.int2byte, ts))
    return (ip_chars + ts_chars)


def maybe_encode(s, encoding='utf8'):
    if isinstance(s, six.text_type):
        s = s.encode(encoding)
    return s


class AuthTKTMiddleware(object):

    """
    Middleware that checks for signed cookies that match what
    `mod_auth_tkt <http://www.openfusion.com.au/labs/mod_auth_tkt/>`_
    looks for (if you have mod_auth_tkt installed, you don't need this
    middleware, since Apache will set the environmental variables for
    you).

    Arguments:

    ``secret``:
        A secret that should be shared by any instances of this application.
        If this app is served from more than one machine, they should all
        have the same secret.

    ``cookie_name``:
        The name of the cookie to read and write from.  Default ``auth_tkt``.

    ``secure``:
        If the cookie should be set as 'secure' (only sent over SSL) and if
        the login must be over SSL. (Defaults to False)

    ``httponly``:
        If the cookie should be marked as HttpOnly, which means that it's
        not accessible to JavaScript. (Defaults to False)

    ``include_ip``:
        If the cookie should include the user's IP address.  If so, then
        if they change IPs their cookie will be invalid.

    ``logout_path``:
        The path under this middleware that should signify a logout.  The
        page will be shown as usual, but the user will also be logged out
        when they visit this page.

    ``digest_algo``:
        Digest algorithm specified as a name of the algorithm provided by
        ``hashlib`` or as a compatible digest object constructor.
        Defaults to ``md5``, as in mod_auth_tkt.  The others currently
        compatible with mod_auth_tkt are ``sha256`` and ``sha512``.

    If used with mod_auth_tkt, then these settings (except logout_path) should
    match the analogous Apache configuration settings.

    This also adds two functions to the request:

    ``environ['paste.auth_tkt.set_user'](userid, tokens='', user_data='')``

        This sets a cookie that logs the user in.  ``tokens`` is a
        string (comma-separated groups) or a list of strings.
        ``user_data`` is a string for your own use.

    ``environ['paste.auth_tkt.logout_user']()``

        Logs out the user.
    """

    def __init__(self, app, secret, cookie_name='auth_tkt', secure=False,
                 include_ip=True, logout_path=None, httponly=False,
                 no_domain_cookie=True, current_domain_cookie=True,
                 wildcard_cookie=True, digest_algo=DEFAULT_DIGEST):
        self.app = app
        self.secret = secret
        self.cookie_name = cookie_name
        self.secure = secure
        self.httponly = httponly
        self.include_ip = include_ip
        self.logout_path = logout_path
        self.no_domain_cookie = no_domain_cookie
        self.current_domain_cookie = current_domain_cookie
        self.wildcard_cookie = wildcard_cookie
        if isinstance(digest_algo, str):
            # correct specification of digest from hashlib or fail
            self.digest_algo = getattr(hashlib, digest_algo)
        else:
            self.digest_algo = digest_algo

    def __call__(self, environ, start_response):
        cookies = request.get_cookies(environ)
        if self.cookie_name in cookies:
            cookie_value = cookies[self.cookie_name].value
        else:
            cookie_value = ''
        if cookie_value:
            if self.include_ip:
                remote_addr = environ['REMOTE_ADDR']
            else:
                # mod_auth_tkt uses this dummy value when IP is not
                # checked:
                remote_addr = '0.0.0.0'
            # @@: This should handle bad signatures better:
            # Also, timeouts should cause cookie refresh
            try:
                timestamp, userid, tokens, user_data = parse_ticket(
                    self.secret, cookie_value, remote_addr, self.digest_algo)
                tokens = ','.join(tokens)
                environ['REMOTE_USER'] = userid
                if environ.get('REMOTE_USER_TOKENS'):
                    # We want to add tokens/roles to what's there:
                    tokens = environ['REMOTE_USER_TOKENS'] + ',' + tokens
                environ['REMOTE_USER_TOKENS'] = tokens
                environ['REMOTE_USER_DATA'] = user_data
                environ['AUTH_TYPE'] = 'cookie'
            except BadTicket:
                # bad credentials, just ignore without logging the user
                # in or anything
                pass
        set_cookies = []

        def set_user(userid, tokens='', user_data=''):
            set_cookies.extend(self.set_user_cookie(
                environ, userid, tokens, user_data))

        def logout_user():
            set_cookies.extend(self.logout_user_cookie(environ))

        environ['paste.auth_tkt.set_user'] = set_user
        environ['paste.auth_tkt.logout_user'] = logout_user
        if self.logout_path and environ.get('PATH_INFO') == self.logout_path:
            logout_user()

        def cookie_setting_start_response(status, headers, exc_info=None):
            headers.extend(set_cookies)
            return start_response(status, headers, exc_info)

        return self.app(environ, cookie_setting_start_response)

    def set_user_cookie(self, environ, userid, tokens, user_data):
        if not isinstance(tokens, six.string_types):
            tokens = ','.join(tokens)
        if self.include_ip:
            remote_addr = environ['REMOTE_ADDR']
        else:
            remote_addr = '0.0.0.0'
        ticket = AuthTicket(
            self.secret,
            userid,
            remote_addr,
            tokens=tokens,
            user_data=user_data,
            cookie_name=self.cookie_name,
            secure=self.secure)
        # @@: Should we set REMOTE_USER etc in the current
        # environment right now as well?
        cur_domain = environ.get('HTTP_HOST', environ.get('SERVER_NAME'))
        wild_domain = '.' + cur_domain

        cookie_options = ""
        if self.secure:
            cookie_options += "; secure"
        if self.httponly:
            cookie_options += "; HttpOnly"

        cookies = []
        if self.no_domain_cookie:
            cookies.append(('Set-Cookie', '%s=%s; Path=/%s' % (
                self.cookie_name, ticket.cookie_value(), cookie_options)))
        if self.current_domain_cookie:
            cookies.append(('Set-Cookie', '%s=%s; Path=/; Domain=%s%s' % (
                self.cookie_name, ticket.cookie_value(), cur_domain,
                cookie_options)))
        if self.wildcard_cookie:
            cookies.append(('Set-Cookie', '%s=%s; Path=/; Domain=%s%s' % (
                self.cookie_name, ticket.cookie_value(), wild_domain,
                cookie_options)))

        return cookies

    def logout_user_cookie(self, environ):
        cur_domain = environ.get('HTTP_HOST', environ.get('SERVER_NAME'))
        wild_domain = '.' + cur_domain
        expires = 'Sat, 01-Jan-2000 12:00:00 GMT'
        cookies = [
            ('Set-Cookie', '%s=""; Expires="%s"; Path=/' % (self.cookie_name, expires)),
            ('Set-Cookie', '%s=""; Expires="%s"; Path=/; Domain=%s' %
             (self.cookie_name, expires, cur_domain)),
            ('Set-Cookie', '%s=""; Expires="%s"; Path=/; Domain=%s' %
             (self.cookie_name, expires, wild_domain)),
            ]
        return cookies


def make_auth_tkt_middleware(
    app,
    global_conf,
    secret=None,
    cookie_name='auth_tkt',
    secure=False,
    include_ip=True,
    logout_path=None):
    """
    Creates the `AuthTKTMiddleware
    <class-paste.auth.auth_tkt.AuthTKTMiddleware.html>`_.

    ``secret`` is required, but can be set globally or locally.
    """
    from paste.deploy.converters import asbool
    secure = asbool(secure)
    include_ip = asbool(include_ip)
    if secret is None:
        secret = global_conf.get('secret')
    if not secret:
        raise ValueError(
            "You must provide a 'secret' (in global or local configuration)")
    return AuthTKTMiddleware(
        app, secret, cookie_name, secure, include_ip, logout_path or None)
