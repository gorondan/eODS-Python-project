import random
import secrets
from beacon_chain_accounting import BeaconChainAccounting
from delegators_registry import DelegatorsRegistry
import delegators_registry
from validators_registry import ValidatorsRegistry
import simulation_constants as constants
from validator import Validator
import validators_registry

class Simulator: 
    beacon_chain_accounting: BeaconChainAccounting
    
    def __init__(self, beacon_chain_accounting):
        self.beacon_chain_accounting = beacon_chain_accounting

    def initialize_required_data(self):
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

            self.beacon_chain_accounting.validators_registry.validators.append(validator)

        # generate the delegators    
        num_delegators_to_generate = random.randint(constants.min_delegators, constants.max_delegators)
        for _ in range(num_delegators_to_generate):
            self.beacon_chain_accounting.delegators_registry.deposit(
                secrets.token_hex(32), 
                random.randint(
                    constants.min_delegator_deposit, 
                    constants.max_delegator_deposit
                    )
                )
    
    def tick_delegation(self):
        num_delegations = random.randint(constants.min_delegations_per_tick, constants.max_delegations_per_tick)
        
        for _ in range(num_delegations):
            delegated_amount = random.randint(constants.min_delegated_amount, constants.max_delegated_amount)
            
            delegator_index = random.randint(0, len(self.beacon_chain_accounting.delegators_registry.delegators)-1)
           
            validator_index = random.randint(0, len(self.beacon_chain_accounting.validators_registry.validators)-1)
            validator = self.beacon_chain_accounting.validators_registry.validators[validator_index]
            validator_key = validator.pubkey
            
            self.beacon_chain_accounting.delegate(delegator_index, validator_key, delegated_amount)

    def process_rewards_penalties(self):
        delegated_validators = self.beacon_chain_accounting.delegated_validators_registry.delegated_validators
        
        for delegated_validator in delegated_validators:
            reward = random.randint(constants.min_reward, constants.max_reward)
            penalties  = random.randint(constants.min_penalty, constants.max_penalty)
            slash  = random.randint(constants.min_slash, constants.max_slash)
            
            probability = random.randint(0,100)
            if(probability >= 99):
                delegated_validator.penalties += slash
            if(probability >= 70):
                delegated_validator.penalties += penalties
            elif(probability >= 30):
                delegated_validator.rewards += reward  
        
        self.beacon_chain_accounting.delegated_validators_registry.process_rewards_penalties()
            