"""
This module simulates an ecosystem in which we can test delegations.
It generates new delegations, applies rewards, penalties, and slashings, 
and processes withdrawals.
"""
import random
import secrets
import math
from eods.beacon_chain_accounting import BeaconChainAccounting
import simulation_constants as constants
from protocol.validator import Validator


class Simulator: 
    """
    The Simulator operates in discrete 'ticks' over a defined number of iterations. 
    During each tick, it generates new delegations, applies rewards, penalties, and slashings, 
    and processes withdrawals.
    """
    beacon_chain_accounting: BeaconChainAccounting
    
    def __init__(self, beacon_chain_accounting):
        self.beacon_chain_accounting = beacon_chain_accounting

   
    def initialize_required_data(self):
        """
        This method generates the initial set of validators and delegators.
        """
        # generate the validators
        num_validators_to_generate = random.randint(constants.min_validators, constants.max_validators)
        
        for _ in range(num_validators_to_generate):
            validator_initial_balance = random.randint(constants.min_validator_initial_balance, constants.max_validator_initial_balance)
            self.beacon_chain_accounting.validators_registry.validators_balances.append(validator_initial_balance)

            validator = Validator()
            validator.pubkey = secrets.token_hex(32)
            validator.effective_balance = validator_initial_balance # + histeresys in the future
            validator.slashed = False
            validator.delegated = False
            validator.fee_percentage = constants.validators_withdrawal_fee_percentage
            self.beacon_chain_accounting.validators_registry.validators.append(validator)

        # generate the delegators    
        num_delegators_to_generate = random.randint(constants.min_delegators, constants.max_delegators)
        for _ in range(num_delegators_to_generate):
            self.beacon_chain_accounting.deposit_to_delegator_balance(
                secrets.token_hex(32), 
                random.randint(
                    constants.min_delegator_deposit, 
                    constants.max_delegator_deposit
                    )
                )
    
    def tick_delegation(self):
        """
        This method creates a random number of delegations with a random amount of delegated GWEI.
        """
        num_delegations = random.randint(constants.min_delegations_per_tick, constants.max_delegations_per_tick)
        
        for _ in range(num_delegations):
            delegated_amount = random.randint(constants.min_delegated_amount, constants.max_delegated_amount)
            
            delegator_index = random.randint(0, len(self.beacon_chain_accounting.delegators_registry.delegators)-1)
           
            validator_index = random.randint(0, len(self.beacon_chain_accounting.validators_registry.validators)-1)
            validator = self.beacon_chain_accounting.validators_registry.validators[validator_index]
            validator_key = validator.pubkey
            
            self.beacon_chain_accounting.delegate_to_validator(delegator_index, validator_key, delegated_amount)

    def tick_withdrawals(self):
        """
        This method creates a random number of withdrawals with a random amount of withdrawed GWEI.
        """
        num_withdrawals = random.randint(constants.min_withdrawals_per_tick, constants.max_withdrawals_per_tick)
        
        for _ in range(num_withdrawals):
            delegated_validator_index = random.randrange(0, len(self.beacon_chain_accounting.delegated_validators_registry.delegated_validators))

            delegated_validator = self.beacon_chain_accounting.delegated_validators_registry.delegated_validators[delegated_validator_index]
            
            matching_indices = [i for i, delegator_balance in enumerate(delegated_validator.delegated_balances) if delegator_balance > 0]

            if len(matching_indices) > 0:

                index = random.randrange(0, len(matching_indices))

                delegator_index = matching_indices[index]
                
                withdrawed_amount = random.randint(0, math.floor(delegated_validator.delegated_balances[delegator_index]))

                self.beacon_chain_accounting.withdraw_from_validator(delegator_index, delegated_validator.delegated_validator.pubkey, withdrawed_amount)
      
    def process_rewards_penalties(self):
        """
        This method generates the rewards, penalties and slashings to be applied to the validator balances.
        """    
        delegated_validators = self.beacon_chain_accounting.delegated_validators_registry.delegated_validators

        for delegated_validator in delegated_validators:
            weight = delegated_validator.validator_balance / constants.MIN_ACTIVATION_BALANCE
            reward = constants.B * weight 
            penalties  = constants.B * weight 
            slash  = random.randint(constants.min_slash, constants.max_slash) * weight
  
            probability = random.randint(0,100)
            if(probability >= 99):
                delegated_validator.penalties += slash
            if(probability >= 70):
                delegated_validator.penalties += penalties
            elif(probability >= 30):
                delegated_validator.rewards += reward
        
        self.beacon_chain_accounting.delegated_validators_registry.process_rewards_penalties()
            