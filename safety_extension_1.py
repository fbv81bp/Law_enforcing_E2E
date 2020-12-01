# This strictly proprietary protocol enables eavesdropping on citizens by centralized but separated authorities.
# Its use is strictly prohibited by the inventor author to any nation, company or individual!
# Application of this protocol or any variants by nations, companies, or individuals are violations of intellectual property laws!

from random import randint as rdi

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

# Alice and Bob perform their personal key exchange with the exponents first agreed upon with the authorities' servers
Alice_Bob_seed = [rdi(100, 1000) for i in range(number_of_authorities)]
Alices_key = Alice_Bob_seed
Bobs_key = Alice_Bob_seed
for rotation in range(number_of_authorities):
    for exchanges in range(number_of_authorities):
        Alices_key[rotation] = Alices_key[rotation] ** Alices_subkeys[exchanges-rotation] % modulus
        Bobs_key[rotation] = Bobs_key[rotation] ** Bobs_subkeys[exchanges-rotation] % modulus
        Alices_key[rotation], Bobs_key[rotation] = Bobs_key[rotation], Alices_key[rotation]

        Alices_key[rotation] = Alices_key[rotation] ** Alices_subkeys[exchanges-rotation] % modulus
        Bobs_key[rotation] = Bobs_key[rotation] ** Bobs_subkeys[exchanges-rotation] % modulus

# Results
print('Communication key material agreed upon by Bob and Alice')
print(Alices_key)
print(Bobs_key)
