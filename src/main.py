from delegated_validator import DelegatedValidator
from validator import Validator

dv = DelegatedValidator(Validator("#123"), 10)

dv.increase_balance(0, 5)
dv.increase_balance(5, 5)
dv.increase_balance(5, 5)