import random
from delegators_registry import DelegatorsRegistry
from validators_registry import ValidatorsRegistry
from simulation_constants import min_validators, max_validators, min_validator_initial_balance, max_validator_initial_balance
from validator import Validator

class Simulator:
    def __init__(self):
        pass

    def initialize_required_data(self, validators_registry: ValidatorsRegistry, delegators_registry: DelegatorsRegistry):
        num_validators_to_generate = random.randint(min_validators, max_validators)
        
        for _ in range(num_validators_to_generate):
            validator_initial_balance = random.randint(min_validator_initial_balance, max_validator_initial_balance)
            validators_registry.validators_balances.append(validator_initial_balance)

            validator = Validator()
            validator.pubkey = f"{random.getrandbits(32):08x}"
            validator.effective_balance = validator_initial_balance # + histeresys in the future
            validator.slashed = False
            validator.delegated = False

            validators_registry.validators.append(validator)
        

        print("done")
