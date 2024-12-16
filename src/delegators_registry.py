from typing import List
from custom_types import Gwei, BLSPubkey
from delegator import Delegator

class DelegatorsRegistry:
    delegators: List[Delegator]  # Stores delegators' data as a list of Delegator instances.
    delegators_balances: List[Gwei]  # List of Gwei delegators' balances

    def __init__(self):
        # Delegators lists initialization
        self.delegators = List[Delegator] = []     
        self.delegators_balances = List[Gwei] = [] # Max size: DELEGATOR_REGISTRY_LIMIT
    
    def delegate_amount(self, delegator_id: BLSPubkey, amount: Gwei):
        delegator_index = self._get_delegator_index_by_id(delegator_id)

        if amount <= 0:
            raise ValueError("Delegated amount must be positive.")

        # Ensure the withdrawal amount does not exceed the delegator's balance in the validator
        if amount > self.delegators_balances[delegator_index]:
            raise ValueError("Delegated amount exceeds the delegator's balance.")
        
        # Removes the delegated amount from the delegator's balance
        self.delegators_balances[delegator_index] -= amount 
        
    def deposit(self, delegator_id: BLSPubkey, amount: Gwei):
        # If delegator does not exist, register the new delegator
        delegator_index = self._get_delegator_index_by_id(delegator_id)
        if delegator_index == -1:
            self._register_delegator(delegator_id)
        
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        # Add the deposit amount to the delegator's balance
        self.delegators_balances[delegator_index] += amount
        
    def _get_delegator_index_by_id(self, delegator_id : BLSPubkey):
        """Helper function to find a validator's index by its ID."""
        delegator_index = -1

        for index, delegator in enumerate(self.delegators):
            if delegator.delegator_id == delegator_id:
               delegator_index = index
               break

        return delegator_index   

    def _register_delegator(self, delegator_id : BLSPubkey):
        """Registers a delegator if not already registered and returns the delegator index."""
        
        # Register new delegator with a zero balance
        new_delegator = Delegator(delegator_id)
        self.delegators.append(new_delegator)
        self.delegators_balances.append(0)

    
        
            
        

        
    
    

        