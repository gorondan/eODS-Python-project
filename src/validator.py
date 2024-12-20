from custom_types import Gwei, BLSPubkey, Epoch, Fee

class Validator:
    def __init__(self):
        self.pubkey = BLSPubkey # Unique identifier for each validator
        self.withdrawal_credentials: bytes = b'\x00' * 32  # Commitment to pubkey for withdrawals
        self.effective_balance = Gwei  # Balance at stake
        self.slashed: bool
        # Status epochs
        self.activation_eligibility_epoch = Epoch  # When criteria for activation were met
        self.activation_epoch = Epoch
        self.exit_epoch = Epoch
        self.withdrawable_epoch = Epoch  # When validator can withdraw funds
        self.delegated: bool # new in eODS
        self.fee_percentage: Fee # new in eODS