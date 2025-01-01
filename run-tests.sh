#!/bin/bash
# This file is part of the CERN Indico plugins.
# Copyright (C) 2014 - 2025 CERN
#
# The CERN Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

for dir in $(find -name pytest.ini -exec dirname {} \;); do
    pushd "$dir" >/dev/null
    pytest "$@"
    popd >/dev/null
done
