#!/usr/bin/python2.7
#
# Helper functions for working with the LinkedIn API.

from linkedin import linkedin


class Error(Exception):
  pass


class LinkedInApiError(Error):
  pass


# TODO(leah): Look at memoizing a bunch of these, so they don't need to run
# as often.
def _GetApiStub(api_key, api_secret, return_url):
  """Returns a stub API object initialized to work with HunchWorks credentials.

  Args:
    api_key: Key to use with the LinkedIn API.
    api_secret: Secret to use to authenticate with the LinkedIn API.
    return_url: URL to return the user to once they've authenticated.

  Returns:
    A LinkedIn API object, authenticated via OAuth.
  """
  api = linkedin.LinkedIn(api_key, api_secret, return_url)
  got_token = api.requestToken()
  if not got_token:
    raise LinkedInApiError('Unable to obtain LinkedIn API stub')

  return api


def GetAuthorizationUrl(api_key, api_secret, return_url):
  """Get's a URL for the user to authorize use of their LinkedIn data.

  Args:
    api_key: Key to use with the LinkedIn API.
    api_secret: Secret to use to authenticate with the LinkedIn API.
    return_url: URL to return the user to once they've authenticated.

  Returns:
    A URL to send the user to so they can authorize use of their LinkedIn data.
  """
  api = _GetApiStub(api_key, api_secret, return_url)
  return api.getAuthorizeURL()


def GetUserConnections():
  """Returns details of the connections for a given user.

  Returns:
    TBD
  """
  pass
