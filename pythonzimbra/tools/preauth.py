""" Preauth Generator """
import codecs
from datetime import datetime
import hashlib
import hmac


def create_preauth(byval, key, by='name', expires=0, timestamp=None):

    """ Generates a zimbra preauth value

    :param byval: The value of the targeted user (according to the
      by-parameter). For example: The account name, if "by" is "name".
    :param key: The domain preauth key (you can retrieve that using zmprov gd)
    :param by: What type is the byval-parameter? Valid parameters are "name"
      (default), "id" and "foreignPrincipal"
    :param expires: Milliseconds when the auth token expires. Defaults to 0
      for default account expiration
    :param timestamp: Current timestamp (is calculated by default)
    :returns: The preauth value to be used in an AuthRequest
    :rtype: str
    """

    if timestamp is None:
        timestamp = int(datetime.now().strftime("%s")) * 1000

    pak = hmac.new(
        codecs.latin_1_encode(key)[0],
        ('%s|%s|%s|%s' % (
            byval,
            by,
            expires,
            timestamp
        )).encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return pak
