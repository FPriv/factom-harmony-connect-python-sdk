#!/usr/bin/env python

import pytest
import sys
import warnings

matplotlib.use('agg')
warnings.filterwarnings("ignore", category=FutureWarning)


pytest.main(['-k-slow', '--cov=factom_sdk'])