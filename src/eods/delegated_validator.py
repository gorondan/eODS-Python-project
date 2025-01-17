"""
This module defines the attributes of class delegated validator.
"""
from typing import List
from eods.custom_types import Gwei, Quota
from protocol.validator import Validator

class DelegatedValidator:
    """
    This class serves as a wrapper around a Validator, providing an abstraction for managing delegated amounts. 
    It adds functionality to the Validator, functionality specific to eODS.
    It defines quotas, tracks balances, and facilitates operations related to delegation management. 
    """
    initial_balance: Gwei
    rewards: Gwei
    penalties: Gwei
    validator_balance: Gwei

    delegated_validator: Validator
    validator_quota: Quota
    delegator_quotas: List[Quota]
    delegated_balances: List[Gwei]
    total_delegated_balance: Gwei
    
    debug_total_rewards: Gwei
    debug_total_penalties: Gwei
    debug_total_delegated: Gwei
    debug_total_withdrawn: Gwei

    def __init__(self, validator: Validator, initial_balance: Gwei):
        self.delegated_validator = validator
        self.initial_balance = initial_balance
        self.validator_balance = self.initial_balance
                
        self.validator_quota = 1
        self.delegator_quotas = [0]
        self.delegated_balances = [0]
        self.total_delegated_balance = 0
        self.rewards = 0
        self.penalties = 0

        self.debug_total_delegated = 0
        self.debug_total_withdrawn = 0
        self.debug_total_rewards = 0
        self.debug_total_penalties = 0
        

    def process_withdrawal(self, delegator_index: int, amount: Gwei) -> Gwei:
        """
        Method to process a withdrawal of balance from the delegated validator towards a delegator with `delegator_index`
        """

        if amount > self.delegated_balances[delegator_index]:
            amount = self.delegated_balances[delegator_index]     

        withdrawable_amount = self._calculate_withdrawable_amount(amount)

        self.delegated_balances[delegator_index] -= withdrawable_amount

        self.total_delegated_balance -= withdrawable_amount

        # Decreases the delegated validator's balance with withdrawable amount
        self._decrease_balance(withdrawable_amount)

        self._recalculate_quotas()

        self.debug_total_withdrawn += withdrawable_amount
        
        return withdrawable_amount

    def process_delegation(self, delegator_index: int, amount: Gwei):
        """
        Method to process a delegation from a delegator with `delegator_index` towards the delegated validator
        """
        num_delegated_balances = len(self.delegated_balances)

        if(num_delegated_balances <= delegator_index):
            for _ in range(delegator_index - num_delegated_balances + 1):
                self.delegated_balances.append(0)
        
        self.delegated_balances[delegator_index] += amount

        self.total_delegated_balance += amount

        self._increase_balance(amount)

        self._recalculate_quotas()

        self.debug_total_delegated += amount

    def process_rewards_penalties(self):
        """
        This method processes the rewards and penalties.
        """
        self._adjust_delegated_balances()

        self.debug_total_rewards += self.rewards
        self.debug_total_penalties += self.penalties

        self.rewards = 0
        self.penalties = 0
       
    def _adjust_delegated_balances(self):
        self._increase_balance(self.rewards)
        self._decrease_balance(self.penalties)

        for index in range(len(self.delegator_quotas)):
            self.delegated_balances[index] = self.validator_balance * self.delegator_quotas[index]
        
        self.total_delegated_balance += (1 - self.validator_quota) * self.rewards
        self.total_delegated_balance -= (1 - self.validator_quota) * self.penalties

    def _calculate_withdrawable_amount(self, amount: Gwei):
        withdrawable_amount = amount * (1 - self.delegated_validator.fee_percentage / 100)
        
        return withdrawable_amount

    def _decrease_balance(self, delta: Gwei): 
        self.validator_balance -= delta

    def _increase_balance(self, delta: Gwei):
        self.validator_balance += delta 

    def _recalculate_quotas(self):
        num_delegated_balances = len(self.delegated_balances)
        num_delegator_quotas = len(self.delegator_quotas)

        #adjust for any list size change
        if(num_delegator_quotas < num_delegated_balances):
            for _ in range(num_delegated_balances - num_delegator_quotas):
                self.delegator_quotas.append(0)
        
        # Calculates the validator's quota from from the active balance, based on it's initial balance
        self.validator_quota = 1 if self.total_delegated_balance == 0 else (self.validator_balance - self.total_delegated_balance) / self.validator_balance

        for index, delegated_amount in enumerate(self.delegated_balances):
            self.delegator_quotas[index] = 0 if self.validator_balance ==0 or self.total_delegated_balance  == 0 else delegated_amount / self.validator_balance
    