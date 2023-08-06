from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re


def parseVersion(versionString):
  """Parse a DIRAC-style version sting

  :param versionString: Version identifier to parse
  :returns: `tuple` of 4 values (major, minor, patch, pre). All values will be
            `int` except "pre" which is `None` for released versions.
  :raises: ValueError if the versionString is invalid
  """
  match = re.match(
      r"^v(?P<major>\d+)r(?P<minor>\d+)(?:p(?P<patch>\d+))?(?:-pre(?P<pre>\d+))?$",
      versionString,
  )
  if not match:
    raise ValueError("%s is not a valid version" % versionString)

  segments = match.groupdict()
  for k, v in segments.items():
    if k != "pre" and v is None:
      segments[k] = 0
    if v is not None:
      segments[k] = int(v)

  return (segments["major"], segments["minor"], segments["patch"], segments["pre"])
