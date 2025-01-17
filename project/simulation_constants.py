"""
This module defines the constants used by the project's simulator, to generate data.
"""
min_validators = 128
max_validators = 1024
 
min_validator_initial_balance = 32
max_validator_initial_balance = 2048

min_delegators = 128
max_delegators = 512

min_delegator_deposit = 32
max_delegator_deposit = 2048

min_delegations_per_tick = 0
max_delegations_per_tick = 16

min_delegated_amount = 1
max_delegated_amount = 2048

min_withdrawals_per_tick = 0
max_withdrawals_per_tick = 16

min_withdrawals_amount = 1
max_withdrawals_amount = 2048

num_ticks = 100

MIN_ACTIVATION_BALANCE = 32
MAX_EFFECTIVE_BALANCE_ELECTRA = 2048

# Rewards and penalties

EFFECTIVE_BALANCE_INCREMENT = 1

B = 32 * EFFECTIVE_BALANCE_INCREMENT / 1e9 # Base reward

min_slash = 1
max_slash = 16

# Fee that Operators recceive for running validators as agents for Delegators

validators_withdrawal_fee_percentage = 10