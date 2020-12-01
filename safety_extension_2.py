# This strictly proprietary protocol enables eavesdropping on citizens by centralized but separated authorities.
# Its use is strictly prohibited by the inventor author to any nation, company or individual!
# Application of this protocol or any variants by nations, companies, or individuals are violations intellectual of property laws!

from random import randint as rdi
from hashlib import sha256 as hash_func 

number_of_authorities = 3 # arbitrary

modulus = 1019 #some large Sophie-Germain prime

# Alices agrees upon her E2E key establishment subkeys with separate state powers' servers
state_and_Alices_seeds = [rdi(100, 1000) for i in range(number_of_authorities)]
Alices_homeland_powers_keys = state_and_Alices_seeds
Alices_subkeys = state_and_Alices_seeds

# performing number_of_authorities DH key exchanges with number_of_authorities separate authorities
for power_branch in range(number_of_authorities):
    power_branchs_exp = rdi(100, 1000)
    Alices_exponent = rdi(100, 1000)
    Alices_subkeys[power_branch] = Alices_subkeys[power_branch] ** Alices_exponent % modulus
    Alices_homeland_powers_keys[power_branch] = Alices_homeland_powers_keys[power_branch] ** power_branchs_exp % modulus
    Alices_subkeys[power_branch], Alices_homeland_powers_keys[power_branch] = Alices_homeland_powers_keys[power_branch], Alices_subkeys[power_branch]
    Alices_subkeys[power_branch] = Alices_subkeys[power_branch] ** Alices_exponent % modulus
    Alices_homeland_powers_keys[power_branch] = Alices_homeland_powers_keys[power_branch] ** power_branchs_exp % modulus

# Results
print()
print('Alices subkeys agreed upon with state')
print(Alices_homeland_powers_keys)
print(Alices_subkeys)
        
# Bob agrees upon his E2E key establishment subkeys with separate state powers' servers
state_and_Bobs_seeds = [rdi(100, 1000) for i in range(number_of_authorities)]
Bobs_homeland_powers_keys = state_and_Bobs_seeds
Bobs_subkeys = state_and_Bobs_seeds

# performing number_of_authorities DH key exchanges with number_of_authorities separate authorities
for power_branch in range(number_of_authorities):
    power_branchs_exp = rdi(100, 1000)
    Bobs_exponent = rdi(100, 1000)
    Bobs_subkeys[power_branch] = Bobs_subkeys[power_branch] ** Bobs_exponent % modulus
    Bobs_homeland_powers_keys[power_branch] = Bobs_homeland_powers_keys[power_branch] ** power_branchs_exp % modulus
    Bobs_subkeys[power_branch], Bobs_homeland_powers_keys[power_branch] = Bobs_homeland_powers_keys[power_branch], Bobs_subkeys[power_branch]
    Bobs_subkeys[power_branch] = Bobs_subkeys[power_branch] ** Bobs_exponent % modulus
    Bobs_homeland_powers_keys[power_branch] = Bobs_homeland_powers_keys[power_branch] ** power_branchs_exp % modulus

# Results
print('Bobs subkeys agreed upon with state')
print(Bobs_homeland_powers_keys)
print(Bobs_subkeys)

# hashing the subkeys agreed upon with authorities, with some cryptographycally secure hash, in order to:
# 1) ensure non of them can individually eavesdrop the communication
# 2) enable a single endpoint's authorities to crack the communication
# 3) enable the number of authorities to be asymmetric
# +1) decrease the necessary computation amount in the final key agreement dircetly performed between Alice and Bob

Alices_string = ''
Bobs_string = ''
for exchanges in range(number_of_authorities):
    Alices_string += str(Alices_subkeys[exchanges])
    Bobs_string += str(Bobs_subkeys[exchanges])

print("Hashes' inputs:", Alices_string, Bobs_string)

Alices_hash = hash_func(Alices_string.encode('utf-8'))
Alices_hash = int.from_bytes(Alices_hash.digest(), byteorder='big', signed=False)
Alices_hash %= modulus

Bobs_hash = hash_func(Bobs_string.encode('utf-8'))
Bobs_hash = int.from_bytes(Bobs_hash.digest(), byteorder='big', signed=False) 
Bobs_hash %= modulus

print('Hashes:', Alices_hash, Bobs_hash)

# Alice and Bob perform their personal key exchange with the exponents first agreed upon with the authorities' servers
Alice_Bob_seed = rdi(100, 1000)
Alices_key = Alice_Bob_seed
Bobs_key = Alice_Bob_seed

# Diffie-Hellman first step
Alices_key = Alices_key ** Alices_hash % modulus
Bobs_key = Bobs_key ** Bobs_hash % modulus
# Diffie-Hellmann exchange
Alices_key, Bobs_key = Bobs_key, Alices_key
# Diffie-Hellman second step
Alices_key = Alices_key ** Alices_hash % modulus
Bobs_key = Bobs_key ** Bobs_hash % modulus

# Results
print('Communication key material agreed upon by Bob and Alice')
print(Alices_key)
print(Bobs_key)
