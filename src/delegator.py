import numpy as np
from custom_types import Gwei, BLSPubkey, Epoch

class Delegator:
    def __init__(self):
        self.pubkey = BLSPubkey # Unique identifier for each validator
        self.withdrawal_credentials: bytes = b'\x00' * 32  # Commitment to pubkey for withdrawals
        self.delegated_balance =  Gwei  # Balance at stake
         # Status epochs
        self.activation_epoch = Epoch
        self.exit_epoch = Epoch
