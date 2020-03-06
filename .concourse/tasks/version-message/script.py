#!/usr/bin/env python
import json
import os

from string import Template

message_template = """:female-detective: A deployment of $host has been detected.
Tests have been started in CircleCI. Check progress here: $circle_url
"""

template = Template(message_template)

with open("./listen-os-cms/message_text_0", "r") as infile:
    host = infile.read()

with open("./circleci-output/build-url.txt", "r") as infile:
    circle_url = infile.read()

print(
    template.substitute(
        host=host,
        circle_url=circle_url,
    )
)
