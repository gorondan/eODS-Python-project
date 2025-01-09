import math
from eods.beacon_chain_accounting import BeaconChainAccounting

class Tester:
    beacon_chain_accounting: BeaconChainAccounting
    
    def __init__(self, beacon_chain_accounting):
        self.beacon_chain_accounting = beacon_chain_accounting
        
    def test_quotas_sum_to_be_1(self):
        delegated_validators = self.beacon_chain_accounting.delegated_validators_registry.delegated_validators
        
        for delegated_validator in delegated_validators:
            sum_quota = 0
            
            for quota in delegated_validator.delegator_quotas:
                sum_quota += quota
                
            sum_quota += delegated_validator.validator_quota

            if(math.isclose(sum_quota, 1, rel_tol=0, abs_tol=1e-8) == False):
                print(sum_quota)
                return False  
        return True
     
    def test_delegated_amount_is_positive(self):
        delegated_validators = self.beacon_chain_accounting.delegated_validators_registry.delegated_validators
        
        for delegated_validator in delegated_validators:
            for amount in delegated_validator.delegated_balances:
                if amount < 0:
                    return False
                
        return True 