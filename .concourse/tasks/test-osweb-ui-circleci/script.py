#!/usr/bin/env python
import json
import os
import sys

import requests

CIRCLE_API_TOKEN = os.environ["CIRCLE_API_TOKEN"]
CIRCLE_JOB = "test-web"
CIRCLE_API_URL = f"https://circleci.com/api/v1.1/project/github/" \
                   f"openstax/os-automation/tree/master?circle-token={CIRCLE_API_TOKEN}"

INSTANCE_MAPPING = {
    "cms-qa": "qa",
    "cms-dev": "dev",
    "cms-staging": "staging",
    "openstax.org": "prod",
}


def log(message, file=sys.stderr):
    print(message, file=file)


def read_file(filepath):
    with open(filepath, "r") as infile:
        data = infile.read()
    return data


def parse_instance(instance_str):
    return INSTANCE_MAPPING[instance_str]


full_message = read_file("./listen-os-cms/message_text")
log(f"Processing message from #deployments: '{full_message}'")

instance = parse_instance(read_file("./listen-os-cms/message_text_0"))
log(f"Instance detected: {instance}")

commit_sha = read_file("./listen-os-cms/message_text_1").split("@")[1]
log(f"Running tests for commit sha: {commit_sha}")

headers = {"Content-Type": "application/json"}

data = {"build_parameters":
    {
        "CIRCLE_JOB": CIRCLE_JOB,
        "INSTANCE": instance
    }
}

r = requests.post(CIRCLE_API_URL, headers=headers, data=json.dumps(data))

r.raise_for_status()

r = r.json()

build_url = r["build_url"]
log(f"Build URL returned by CircleCI is: {build_url}")

with open("./circleci-output/build-url.txt", "w") as outfile:
    outfile.write(build_url)
