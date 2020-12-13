# This strictly proprietary protocol enables eavesdropping on citizens by centralized but separated authorities.
# Its use is strictly prohibited by the inventor author to any nation, company or individual!
# Application of this protocol or any variants by nations, companies, or individuals are violations of intellectual property laws!

from random import randint as rdi
from hashlib import sha256 as hash_func 


''' CONFIGURATION '''

# number of separate authority sets, for example different nations
number_of_nations = 5 # can be any random number

# numbers of theoretically independent authorities in each nation, that the group communication is taking place at
number_of_authorities = [5,3,7,4,2] # can be diverse random numbers

# number of people communicating in a group, who must share the same final key for the communication
number_of_participants = 12 # can be any random number

# which set of authorities a certain participant has to agree upon sub key values
participants_nationality = [1,3,0,1,4,1,0,2,4,3,0,1] # a list containing indexes of the authority sets' nationalities

# pre-agreed parameters of the Diffie-Hellman key exchange
modulus = 1019 # should be a large safe prime (more like 2^4096 sized Sophie-Germain prime)


''' PROTOCOL DESCRIPTION'''

# two party Diffie-Hellman key exchange for calculating the keys with the authorities: here with modular exponentiation
def Diffie_Hellman_for_2(seed, modulus, party_A_secret, party_B_secret):
    party_A_key = seed
    party_B_key = seed
    # performing 1st steps of modular exponentiation
    party_A_key = pow(party_A_key, party_A_secret, modulus)
    party_B_key = pow(party_B_key, party_B_secret, modulus)
    # exchanging partian results
    party_A_key, party_B_key = party_B_key, party_A_key
    # performing 2nd steps of modular exponentiation
    party_A_key = pow(party_A_key, party_A_secret, modulus)
    party_B_key = pow(party_B_key, party_B_secret, modulus)
    return party_A_key, party_B_key

# key exchanges between participants and their respective nations' local authorities who will store their portions of keys for
# eavesdropping if the authorities of a certain nation can all agree upon the procedure being legal in their local legislation
nations_powerbranches_keys = [[] for i in range(number_of_nations)]
participants_subkeys = []
for participants_nation in participants_nationality:
    single_power_branchs_keys = []
    single_participants_subkeys = []
    for power_branch in range(number_of_authorities[participants_nation]):
        seed_between_participant_and_one_power_branch = rdi(100,1000)
        power_branchs_secret = rdi(100, 1000)
        participants_secret = rdi(100, 1000)
        # performing Diffie-Hellmans
        powers_keys, participants_subkey = Diffie_Hellman_for_2(seed_between_participant_and_one_power_branch, modulus, power_branchs_secret, participants_secret)
        # collecting derived keys accordingly
        single_power_branchs_keys.append(powers_keys)
        single_participants_subkeys.append(participants_subkey)
    # collecting the distributed sub-key rings accordingly
    nations_powerbranches_keys[participants_nation].append(single_power_branchs_keys)
    participants_subkeys.append(single_participants_subkeys)

# Results
print()
for nation in nations_powerbranches_keys:
    print()
    print('national key collections')
    for link in nation:
        print("link's sub keys")
        print(link)
print()
for participant in participants_subkeys:
    print('participants own subkeys')
    print(participant)

# hashing the subkeys agreed upon with authorities, with some cryptographycally secure hash, in order to:
# 1) ensure non of them can individually eavesdrop the communication
# 2) enable a single endpoint's authorities to crack the communication
# 3) enable the number of authorities to be asymmetric in the different nations
# +1) decrease the necessary computation amount in the final key agreement dircetly performed between Alice and Bob

# concatenating subkeys that were agreed with someone's local authorities for hashing
participants_hash_inputs = []
participants_hashes = [0 for i in range(number_of_participants)]
for participant_subkeys in participants_subkeys:
    hash_input = ''
    for subkey in participant_subkeys:
        hash_input += str(subkey)
    participants_hash_inputs.append(hash_input)

# Results    
print()
print("hashes' inputs")
print(participants_hash_inputs)

# hashing
for participant_index in range(number_of_participants):
     # any encoding as long as it is standardized
    participants_hashes[participant_index] = hash_func(participants_hash_inputs[participant_index].encode('utf-8'))
    # any endianness or signedness as long as they're standardized
    participants_hashes[participant_index] = int.from_bytes(participants_hashes[participant_index].digest(), byteorder='big', signed=False)
    # may be omitted if hash results are smaller than the modulus by default
    participants_hashes[participant_index] %= modulus

# Results
print()
print("hashes' outputs")
print(participants_hashes)

# multi-party Diffie-Hellman key exchange for calculating the final key between the communicating oarties: here with modular exponentiation
def multi_party_Diffie_Hellman(partys_keys, modulus, parties_secrets):
    # we need as many key exchanges as there are participants in the communication group
    for j in range(len(partys_keys)):    
        # performing modular exponentiations
        for i in range(len(parties_secrets)):
            partys_keys[i] = pow(partys_keys[i], parties_secrets[i], modulus)
        # exchanging partial results
        partys_keys = [partys_keys[k-1] for k in range(len(partys_keys))]
    return partys_keys
    
# participants perform their personal key exchange with their respective hash as exponent,whose inputs were first agreed upon with their
# respective local authorities' servers
all_participants_seed = rdi(100, 1000)
participants_keys = [all_participants_seed for i in range(number_of_participants)]
participants_keys = multi_party_Diffie_Hellman(participants_keys, modulus, participants_hashes)

# Results
print()
print('final communication keys')
print(participants_keys)

# national sets of authorities can individually compute the hashes used by individuals on their territory and calculate the last Diffie-Hellman
# step of the key exchange if they have first observed the key exchange's last step