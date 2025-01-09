import sys
from typing import List
from eods.custom_types import Gwei, Quota
from protocol.validator import Validator

class DelegatedValidator:
    initial_value: Gwei
    rewards: Gwei
    penalties: Gwei
    validator_balance: Gwei

    delegated_validator: Validator
    delegator_quotas: List[Quota]
    delegated_balances: List[Gwei]

    def __init__(self, validator: Validator, initial_value: Gwei):
        self.delegated_validator = validator
        self.initial_value = initial_value
        
        self.delegator_quotas = [0]
        self.delegated_balances = [0]
        self.rewards = 0
        self.penalties = 0
        self.validator_balance = initial_value

    def process_withdrawal(self, delegator_index: int, amount: Gwei):
        """
        Method to process a withdrawal of balance from the delegated validator towards a delegator with `delegator_index`
        """
        withdrawable_amount = self._calculate_withdrawable_amount(amount)

        # Deducts the withdrawed amount from the delegated balances with underflow protection
        self.delegated_balances[delegator_index] = 0 if withdrawable_amount > self.delegated_balances[delegator_index] else self.delegated_balances[delegator_index] - withdrawable_amount
        
        self._decrease_balance(amount)

        self._recalculate_quotas()

    def process_delegation(self, delegator_index: int, amount: Gwei):
        """
        Method to process a delegation from a delegator with `delegator_index` towards the delegated validator
        """
        num_delegated_balances = len(self.delegated_balances)

        if(num_delegated_balances <= delegator_index):
            for _ in range(delegator_index - num_delegated_balances + 1):
                self.delegated_balances.append(0)
        
        self.delegated_balances[delegator_index] += amount

        self._increase_balance(amount)

        self._recalculate_quotas()

    def process_rewards_penalties(self):
        self._adjust_delegated_balances()
        self.rewards = 0
        self.penalties = 0
       
    def _adjust_delegated_balances(self):
        self._increase_balance(self.rewards)
        self._decrease_balance(self.penalties)
        
        for index in range(len(self.delegator_quotas)):
            self.delegated_balances[index] = (self.validator_balance - self.initial_value) * self.delegator_quotas[index]

    def _calculate_withdrawable_amount(self, amount: Gwei):
        withdrawable_amount = amount * (1 - self.delegated_validator.fee_percentage / 100)
        
        return withdrawable_amount

    def _decrease_balance(self, delta: Gwei):
        """
        Method to decrease the delegated validator's balance with `delta`, with underflow protection
        """
        
        self.validator_balance = 0 if delta > self.validator_balance else self.validator_balance - delta

    def _increase_balance(self, delta: Gwei):
        """
        Method to increase the delegated validator's balance with `delta` 
        """
        self.validator_balance += delta 

    def _recalculate_quotas(self):
        num_delegated_balances = len(self.delegated_balances)
        num_delegator_quotas = len(self.delegator_quotas)

        #adjust for any list size change
        if(num_delegator_quotas < num_delegated_balances):
            for _ in range(num_delegated_balances - num_delegator_quotas):
                self.delegator_quotas.append(0)

        for index, delegated_amount in enumerate(self.delegated_balances):
            self.delegator_quotas[index] = delegated_amount / (self.validator_balance - self.initial_value)
    