#!/usr/bin/env python

import pytest
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


pytest.main(['-k-slow', '--cov=factom_sdk'])