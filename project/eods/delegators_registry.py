"""
This module modifies the state of the delegators registry.
"""
from typing import List
from eods.custom_types import Gwei, BLSPubkey, DelegatorIndex
from eods.delegator import Delegator


class DelegatorsRegistry:
    """
    This class defines the registry used to manage delegators.
    """
    delegators: List[Delegator]  # Stores delegators' data as a list of Delegator instances.
    delegators_balances: List[Gwei]  # List of Gwei delegators' balances

    def __init__(self):
        # Delegators lists initialization
        self.delegators = []
        self.delegators_balances = [] # Max size: DELEGATOR_REGISTRY_LIMIT

    def decrease_delegator_balance(self, delegator_index: DelegatorIndex, amount: Gwei):
        """
        This method removes an amount from a delegator's balance.
        """
        self.delegators_balances[delegator_index] -= amount    

    def deposit(self, pubkey: BLSPubkey, amount: Gwei):
        """
        This method adds an amount to a delegator's balance.
        If there is no delegator for the specified pubkey, a delegator will be created.
        """
        
        # If delegator does not exist, register the new delegator
        delegator_index = self._get_delegator_index_by_id(pubkey)
        if delegator_index == -1:
            self._register_delegator(pubkey)

        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        # Add the deposit amount to the delegator's balance
        self.delegators_balances[delegator_index] += amount

    def increase_delegator_balance(self, delegator_index: DelegatorIndex, amount: Gwei):
        """
        This method adds an amount to a delegator's balance.
        """

        if amount < 0:
            raise ValueError("Amount must be positive.")

        self.delegators_balances[delegator_index] += amount

    def withdraw(self, pubkey: BLSPubkey, amount: Gwei):
        """
        This method withdraws an amount from a delegator's balance.
        If the requested amount is larger than the available amount, 
        only the available amount will be returned.
        """
        
        delegator_index = self._get_delegator_index_by_id(pubkey)

        amount_to_withdraw = amount

        if(amount_to_withdraw > self.delegators_balances[delegator_index]):
            amount_to_withdraw = self.delegators_balances[delegator_index]
            
        self.delegators_balances[delegator_index] -= amount_to_withdraw

    def _get_delegator_index_by_id(self, pubkey : BLSPubkey):
        """Helper function to find a validator's index by its ID."""
        delegator_index = -1

        for index, delegator in enumerate(self.delegators):
            if delegator.pubkey == pubkey:
                delegator_index = index
                break

        return delegator_index

    def _register_delegator(self, pubkey : BLSPubkey):
        """Registers a delegator if not already registered and returns the delegator index."""

        # Register new delegator with a zero balance
        new_delegator = Delegator()
        new_delegator.pubkey = pubkey

        self.delegators.append(new_delegator)
        self.delegators_balances.append(0)
