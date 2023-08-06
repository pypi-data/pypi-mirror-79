from __future__ import absolute_import
from __future__ import print_function

import argparse
import json
import os
import sys

from .cfg import CFG
from .versions import parseVersion


def parseArgs():
  parser = argparse.ArgumentParser(description='Parser for DIRAC cfg files')
  subparsers = parser.add_subparsers(help='Actions to run with the ')

  parserJson = subparsers.add_parser('as-json', help='Dump the entire configuration as JSON')
  parserJson.add_argument('cfgfile')
  parserJson.set_defaults(func=lambda a: dumpAsJson(a.cfgfile))

  parserSort = subparsers.add_parser(
      'sort-versions',
      help='Read JSON from stdin and prints JSON list of sorted version numbers'
  )
  parserSort.add_argument('--allow-pre-releases', action='store_true')
  parserSort.set_defaults(func=lambda a: sortVersions(a.allow_pre_releases))

  args = parser.parse_args()
  args.func(args)
  # Explicitly exit to make testing easier
  sys.exit(0)


def dumpAsJson(cfgFilename):
  if not os.path.isfile(cfgFilename):
    sys.stderr.write('ERROR: %s does not exist\n' % cfgFilename)
    sys.exit(1)
  res = CFG().loadFromFile(cfgFilename)
  print(json.dumps(res.getAsDict()))


def sortVersions(allow_pre_releases=False):
  try:
    objs = json.loads(sys.stdin.read())
  except getattr(json, 'JSONDecodeError', ValueError):
    sys.stderr.write('ERROR: Failed to parse standard input as JSON\n')
    sys.exit(3)

  parsedVersions = {}
  for obj in objs:
    try:
        major, minor, patch, pre = parseVersion(obj)
    except ValueError:
      if obj not in ('integration', 'devel', 'master'):
        sys.stderr.write('WARN: Unexpected version string %r\n' % obj)
    else:
      if pre is None:
        pre = sys.maxsize
      elif not allow_pre_releases:
        continue
      parsedVersions[obj] = (major, minor, patch, pre)

  print(json.dumps(sorted(parsedVersions, key=parsedVersions.get, reverse=True)))


if __name__ == '__main__':
  parseArgs()   # pragma: no cover
