#! /usr/bin/env python
#  -*- coding: utf-8 -*-

from optparse import OptionParser
import xml.etree.cElementTree as ET
import sys
from os import isatty

__version__ = "0.6"
"""Version of lib"""


def version():
    """
    Returns version of libary

    :return: Version of lib as String
    """
    return __version__


def is_pipe():
    """
    Return if stdin has a value

    :return: True, if there is a value on stdin
    """
    return not isatty(sys.stdin.fileno())


def main():
    """
    Main Method of lib
    """

    # detecting if script was run interactively
    junit_xml_output = "yamllint-junit.xml"

    parser = OptionParser(
        usage="%prog [yamllint-junit output file] [options]",
        version="%prog " + version()
    )

    parser.add_option("-o", "--output", action="store", dest="output_file", help="output XML to file",
                      default=junit_xml_output)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="print XML to console as command output", default=False)

    (options, args) = parser.parse_args()

    lines = []
    if is_pipe():
        for line in sys.stdin:
            if len(line.strip()) > 0:
                lines.append(line.strip())

    if len(lines) == 0 and (len(args) == 0 or not args[0]):
        parser.print_help()
        parser.error('You need to provide file with output or pipe data from "yamllint" command.')
        exit(1)

    if len(lines) == 0:
        ansible_lint_output = open(args[0], "r").read().split("\n")

        for line in ansible_lint_output:
            if len(line.strip()) > 0:
                lines.append(line.strip())

    testsuites = ET.Element("testsuites")

    errors_count = str(len(lines))

    testsuite = ET.SubElement(testsuites, "testsuite", errors=errors_count, failures="0", tests=errors_count, time="0")

    if 0 == len(lines):
        ET.SubElement(testsuite, "testcase", name="dummy_testcase.py")
    else:
        parsed_lines = []
        for line in lines:
            parsed_line = line.split(":")

            line_data = {
                "filename": parsed_line[0],
                "line": int(parsed_line[1]),
                "error": {
                    "message": parsed_line[3].strip(),
                    "text": "[%s:%s] %s" % (parsed_line[1], parsed_line[2], parsed_line[3].strip())
                }
            }
            parsed_lines.append(line_data)

            testcase = ET.SubElement(testsuite, "testcase", name=line_data['filename'])
            ET.SubElement(
                testcase,
                "failure",
                file=line_data['filename'],
                line=str(line_data['line']),
                message=line_data['error']['text'],
                type="YAML Lint"
            ).text = line_data['error']['text']

    tree = ET.ElementTree(testsuites)
    tree.write(options.output_file, encoding='utf8', method='xml')
    parsed_lines_xml = ET.tostring(testsuites, encoding='utf8', method='xml')

    if options.verbose:
        print(parsed_lines_xml)
