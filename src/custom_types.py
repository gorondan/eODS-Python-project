import numpy as np

# State list lengths
VALIDATOR_REGISTRY_LIMIT = 100  # Validator registry size limit
DELEGATOR_REGISTRY_LIMIT = 100  # Delegator registry size limit


# Custom types
Gwei = np.uint64
Epoch = np.uint64
Fee =  np.uint
Quota =  np.uint
delegator_index = np.uint
validator_index = np.uint