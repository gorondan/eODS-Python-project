import random
import secrets
from delegators_registry import DelegatorsRegistry
from validators_registry import ValidatorsRegistry
import simulation_constants as constants
from validator import Validator

class Simulator: 
    def __init__(self):
        pass

    def initialize_required_data(self, validators_registry: ValidatorsRegistry, delegators_registry: DelegatorsRegistry):
        # generate the validators
        num_validators_to_generate = random.randint(constants.min_validators, constants.max_validators)
        
        for _ in range(num_validators_to_generate):
            validator_initial_balance = random.randint(constants.min_validator_initial_balance, constants.max_validator_initial_balance)
            validators_registry.validators_balances.append(validator_initial_balance)

            validator = Validator()
            validator.pubkey = secrets.token_hex(32)
            validator.effective_balance = validator_initial_balance # + histeresys in the future
            validator.slashed = False
            validator.delegated = False

            validators_registry.validators.append(validator)

        # generate the delegators    
        num_delegators_to_generate = random.randint(constants.min_delegators, constants.max_delegators)
        for _ in range(num_delegators_to_generate):
            delegators_registry.deposit(
                secrets.token_hex(32), 
                random.randint(constants.min_delegator_deposit, constants.max_delegator_deposit)
                )
    
    def tick_delegation(self):
        pass    