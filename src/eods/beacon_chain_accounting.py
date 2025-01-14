from protocol.validators_registry import ValidatorsRegistry
from eods.delegated_validators_registry import DelegatedValidatorsRegistry
from eods.delegators_registry import DelegatorsRegistry
from eods.custom_types import BLSPubkey, Gwei, DelegatorIndex

class BeaconChainAccounting:
    """
    This class is responsible for exposing the balance sheet operations - delegations and withdrawals.
    """
    
    delegators_registry: DelegatorsRegistry
    validators_registry: ValidatorsRegistry

    delegated_validators_registry: DelegatedValidatorsRegistry

    def __init__(self):
        self.delegated_validators_registry = DelegatedValidatorsRegistry()
        self.delegators_registry = DelegatorsRegistry()
        self.validators_registry = ValidatorsRegistry()

    
    def delegate(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        """
        This method acts as an entrypoint for delegation. It creates a delegation if needed and 
        it deposits a given amount.
        
        Args:
            delegator_index (DelegatorIndex): The index of the delegator.
            validator_pubkey (BLSPubkey): The public key of the validator.
            amount (Gwei): The amount delegated.
        """
        
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if not self.delegated_validators_registry.is_validator_delegated(validator.pubkey):
            self.delegated_validators_registry.create_delegated_validator(validator, amount)

        self.delegated_validators_registry.process_delegation(delegator_index, validator.pubkey, amount)

    def withdraw(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        """
        This method acts as an entrypoint for withdrawal. 
        Args:
            delegator_index (DelegatorIndex): The index of the delegator.
            validator_pubkey (BLSPubkey): The public key of the validator.
            amount (Gwei): The amount that whould be withdrawn.
        """
        
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")

        if not self.delegated_validators_registry.is_validator_delegated(validator.pubkey):
            raise ValueError("Validator with the provided pubkey is not delegated validator")

        self.delegated_validators_registry.process_withdrawal(delegator_index, validator.pubkey, amount)
