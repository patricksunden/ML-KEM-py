# Quantumcrypto  
Collection of tools designed to handle cryptography in post quantum computers world.

## Warning: The security cannot be guaranteed. For now, do not use in real projects!  

## ML-KEM

Example 1.  
```python
from quantumcrypto import MLKEM

bob = MLKEM("512")
bob_encapsulation_key, bob_decapsulation_key = bob.generate_keys()

alice = MLKEM("512")
alice_secret_key, cipher = alice.encaps(bob_encapsulation_key)

bob_secret_key = bob.decaps(bob_decapsulation_key, cipher)
assert bob_secret_key == alice_secret_key
```

The parameter options for MLKEM are 512 | 768 | 1024. Anything other will default to the strongest 1024.  
User has to consciously select the weaker (and more performant) option if they want to use it.  

Example 2.  

```python
from quantumcrypto import MLKEM

bob = MLKEM("768")
bob_encapsulation_key, bob_decapsulation_key = bob.generate_keys()

alice = MLKEM("768")
alice_secret_key, cipher = alice.encaps(bob_encapsulation_key)

bob_secret_key = bob.decaps(bob_decapsulation_key, cipher)
assert bob_secret_key == alice_secret_key

mallory = MLKEM("768")
mallory_secret_key, mallory_cipher = mallory.encaps(bob_encapsulation_key)

bob_key2 = bob.decaps(bob_decapsulation_key, mallory_cipher)
assert bob_key2 == mallory_secret_key
assert bob_secret_key != bob_key2
```

Example 3.  
```python
from quantumcrypto import MLKEM

bob = MLKEM("1024")
bob_encapsulation_key, bob_decapsulation_key = bob.generate_keys()

alice = MLKEM("1024")
alice_secret_key, cipher = alice.encaps(bob_encapsulation_key)

bob_secret_key = bob.decaps(bob_decapsulation_key, cipher)
assert bob_secret_key == alice_secret_key

mallory = MLKEM()   # default is 1024
mallory_secret_key, mallory_cipher = mallory.encaps(bob_encapsulation_key)

bob_key2 = bob.decaps(bob_decapsulation_key, mallory_cipher)
assert bob_key2 == mallory_secret_key
assert bob_secret_key != bob_key2
```  

### Description
The implementation of ML-KEM Standard, one of the three Federal Information Processing Standards (FIPS) approved for post-quantum cryptography. 
This standard is specified in [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final).
For this project, the FIPS 203 standard has been implemented for use in a cryptographic library



### Background
A key-encapsulation mechanism (KEM) is a set of algorithms that, under specific conditions, enable two parties to establish a shared secret key over a public channel.

The securely established shared key can then be utilized with symmetric-key cryptographic algorithms to perform fundamental tasks in secure communications, such as encryption and authentication.

Although quantum computers are not yet fully realized, they are believed to have the potential to break existing cryptographic standards. In anticipation of this, NIST has approved three new standards for post-quantum cryptography to ensure the world is prepared when quantum computers become a reality.

Currently, ML-KEM is considered secure, even against adversaries equipped with large-scale, fault-tolerant quantum computers. This standard defines the algorithms and parameter sets for the ML-KEM scheme:

- The three parameter sets, listed in order of increasing security strength and decreasing performance, are:  
    - **ML-KEM-512**,  
    - **ML-KEM-768**,  
    - **and ML-KEM-1024**.  

- The key exchange algorithms specified are for:  
    - **key generation**,  
    - **encapsulation**,  
    - **decapsulation**.


### How the standard has been implemented
All the sub-algorithms have been implemented as functions in Python to realize the three main algorithms:  
- **ML-KEM.generate_keys**,  
- **ML-KEM.encaps**,  
- **ML-KEM.decaps**.  

The parameter sets:  
- **ML-KEM-512**,  
- **ML-KEM-768**,  
- **ML-KEM-1024**  

have also been pre-defined by FIPS 203 standard, allowing users to easily select their desired parameter set based on desired security and performance level.


### Algorithms
ML-KEM operates with three algorithms  

**ML-KEM.generate_keys**  
- Using internally generated randomness and requiring no input, the algorithm produces an **encapsulation key** and a **decapsulation key**. The encapsulation key can be made public, while the decapsulation key shall remain private.  

**ML-KEM.Encaps**  
- The algorithm accepts an encapsulation key as input, generates randomness internally, and outputs a **shared key** and a **ciphertext**. 

**ML-KEM.Decaps**  
- The algorithm accepts a decapsulation key and an ML-KEM ciphertext as input, uses no randomness, and outputs a shared secret key.

### Parameter Sets
To instantiate ML-KEM, the key exchanging parties must agree on used parameter set and the strength of the generated keys. Each parameter set is associated with a particular trade-off between security and performance.
- ML-KEM-512 (security category 1)
- ML-KEM-768 (security category 3)
- ML-KEM-1024 (security category 5)
