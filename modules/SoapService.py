""" SOAP client module  """
import httplib

from config import SERVER_ADR


def shootsoap(body, post_action):
    """ Connects to the iNew service """

    bodylenght = len(body)

    request = httplib.HTTPConnection(SERVER_ADR, 8080)
    request.putrequest("POST", post_action)
    request.putheader("Accept", "application/soap+xml, application/dime, multipart/related, text/*")
    request.putheader("Content-Type", "application/soap+xml;charset=UTF-8")
    request.putheader("Cache-Control", "no-cache")
    request.putheader("Content-Length", str(bodylenght))
    request.endheaders()
    # Commented in case of accidental runs
    request.send(body)
    response = request.getresponse().read()

    return response

