import json
import os
import time
from pathlib import Path
from subprocess import CalledProcessError

import pytest

from dispatch.retry import increase_retry
from common.constants import mercure_names


def test_execute_increase(fs, mocker):
    source = "/var/data"
    fs.create_dir(source)
    target = {"dispatch": {"target_ip": "0.0.0.0", "target_aet_target": "a", "target_port": 90}}
    fs.create_file("/var/data/" + mercure_names.TASKFILE, contents=json.dumps(target))
    result = increase_retry(source, 5, 50)

    with open("/var/data/" + mercure_names.TASKFILE, "r") as f:
        modified_target = json.load(f)

    assert modified_target["dispatch"]["retries"] == 1
    assert modified_target["dispatch"]["next_retry_at"]
    assert result


def test_execute_increase_fail(fs, mocker):
    source = "/var/data"
    fs.create_dir(source)
    target = {
        "dispatch": {
            "target_ip": "0.0.0.0",
            "target_aet_target": "a",
            "target_port": 90,
            "retries": 5,
        }
    }
    fs.create_file("/var/data/" + mercure_names.TASKFILE, contents=json.dumps(target))
    result = increase_retry(source, 5, 50)

    assert not result
