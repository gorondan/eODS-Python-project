"""
This module defines the attributes of class delegator.
"""
from eods.custom_types import Gwei, BLSPubkey, Epoch

class Delegator:
    """
    This class defines the attributes of a new protocol entity (the delegator), that that represents token holders
    who delegate their stake to validators in order to secure the network and earn staking rewards.
    """
    def __init__(self):
        self.pubkey = BLSPubkey # Unique identifier for each delegator
        self.withdrawal_credentials: bytes = b'\x00' * 32  # Commitment to pubkey for withdrawals
        self.delegated_balance =  Gwei  # Delegated balance at stake
        # Status epochs
        self.activation_epoch = Epoch
        self.exit_epoch = Epoch
