"""
This module defines the custom types used by the program.
"""
from typing import ByteString
import numpy as np

Gwei = np.uint64
Epoch = np.uint64
Fee =  np.uint
Quota =  np.uint
BLSPubkey = ByteString
DelegatorIndex = np.uint
ValidatorIndex = np.uint