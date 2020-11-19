from random import randint as rdi

''' CONFIGURATION '''

# number of separate authority sets, for example different nations
number_of_nations = 3 # can be any random number

# number of theoretically independent authorities in every nation the group communication is taking place at
number_of_authorities = 5 # can be any random number

# number of people communicating in a group, who must share the same key for the communication
number_of_participants = 12 # can be any random number

# which set of authorities a certain participant has to agree upon sub key values
participants_nationality = [rdi(0,number_of_nations-1) for i in range(number_of_participants)] # a list containing indexes of authority sets

# pre-agreed modulus of the Diffie-Hellman key exchange
modulus = 1019 # should be a large safe prime (more like 2^4096 sized Sophie-Germain prime)

''' PROTOCOL DESCRIPTION'''

# two party Diffie-Hellman key exchange: here with modular exponentiation
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


nations_powerbranches_keys = [[] for i in range(number_of_nations)]
participants_subkeys = []
for participants_nation in participants_nationality:
    single_power_branchs_keys = []
    single_participants_subkeys = []
    for power_branch in range(number_of_authorities):
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

#Results
print()
for nation in nations_powerbranches_keys:
    print('national key collection')
    for link in nation:
        print("link's sub keys")
        print(link)
print()
for participant in participants_subkeys:
    print('participants own subkeys')
    print(participant)


# multi-party Diffie-Hellman key exchange: here with modular exponentiation
def multi_party_Diffie_Hellman(partys_keys, modulus, parties_secrets):
    # we need as many key exchanges as there are participants in the communication group
    for j in range(len(partys_keys)):    
        # performing modular exponentiations
        for i in range(len(parties_secrets)):
            partys_keys[i] = pow(partys_keys[i], parties_secrets[i], modulus)
        # exchanging partial results
        partys_keys = [partys_keys[k-1] for k in range(len(partys_keys))]
    return partys_keys
    
    
# participants perform their personal key exchange with the exponents first agreed upon with their respective local authorities' servers
all_participants_seed = rdi(100, 1000)
participants_keys = [all_participants_seed for i in range(number_of_participants)]
for exchanges in range(number_of_authorities):
    participants_secrets = [participants_subkeys[person][exchanges] for person in range(number_of_participants)]
    participants_keys = multi_party_Diffie_Hellman(participants_keys, modulus, participants_secrets)

# Results
print()
print('final communication keys')
print(participants_keys)


# proof that all sets of national authorities together can crack the communication provided they have eavesdropped the communication of the initial seed 'all_participants_seed'
nations_key_result = all_participants_seed
for nation in nations_powerbranches_keys:
    for link in nation:
        for subkey in link:
            nations_key_result **= subkey 
            nations_key_result %= modulus 
print('internationally computable communication key:', nations_key_result)
