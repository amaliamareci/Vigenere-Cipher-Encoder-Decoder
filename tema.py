import random
from collections import Counter
letter_to_number = {}
number_to_letter = {}

for i in range(26):
    letter_to_number[chr(ord('A') + i)] = i
    number_to_letter[i] = chr(ord('A') + i)

english_frequencies={'A':0.082 , 'B':0.015 , 'C':0.027 , 'D':0.043 , 'E':0.13 , 'F':0.022 , 'G':0.02 , 'H':0.062 , 'I':0.069 , 'J':0.0015 , 'K':0.0078 , 'L':0.041 , 'M':0.025 , 'N':0.067 , 'O':0.078 , 'P':0.019 , 'Q':0.00096 , 'R':0.059 , 'S':0.062 , 'T':0.096 , 'U':0.027 , 'V':0.0097 , 'W':0.024 , 'X':0.0015 , 'Y':0.02 , 'Z':0.00078}
def Vigenere():
    print("Vigenere Cipher Encoder/Decoder")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("enter 1 to encode a message from input.txt with random key")
    print("enter 2 to encode a message from input.txt with your key")
    print("enter 3 to decode a message with knowing key")
    print("enter 4 to decode a messege without the key")
    print("enter 5 to quit")
    userSelection = input()
    if userSelection == "1":
        plain_text =input_file('input3.txt')
        key=random_key()
        print("the key is :",key)
        key=key.upper()
        cryptotext = ENCRYPTION(plain_text, key, 'encryption.txt')
        print("the encript messege is in encrtption.txt")
        print('Press any key to exit...')
        input()
    if userSelection== "2":
        plain_text = input_file('input3.txt')
        print("Enter the key phrase to use for encrypting:")
        key = input()
        key=key.upper()
        cryptotext = ENCRYPTION(plain_text, key, 'encryption.txt')
        print("the encript messege is in encrtption.txt")
        print('Press any key to exit...')
        input()    
    if userSelection== "3":
        cryptotext=input_file("encryption.txt")
        print("Enter the key number to use for Decrypting:")
        Key = input()
        Key=Key.upper()
        DECRYPTION(cryptotext,Key,'decryption.txt')
        print("the decripted messege is in decryption.txt")
        print('Press any key to exit...')
        input()
    if userSelection== "4":
        cryptotext=input_file("encryption.txt")
        key_length = initinal_key_length(cryptotext)
        found_key = get_key(cryptotext,key_length)
        DECRYPTION(cryptotext,found_key,'decryption.txt')
        print('KEY: ',found_key)
        print("the decripted messege is in decryption.txt")
        print('Press any key to exit...')
        input()

#filter the input so it has only big letters
def input_file(file_name):
    file = open(file_name, "r")
    text = ''
    for c in file.read():
        if c == c.lower():
            c = c.upper()
        if c >= 'A' and c <= 'Z':
            text += c
    file.close()
    return text

#encrypting a plaintext using a key
def ENCRYPTION(plaintext, key, output_file_name):
    cryptotext = ''
    m = len(key)
    for i in range(len(plaintext)):
        cryptotext += number_to_letter[(letter_to_number[plaintext[i]] + letter_to_number[key[i % m]]) % 26]

    output_file = open(output_file_name, "w")
    output_file.write(cryptotext)
    output_file.close()

#deencrypting a plaintext using a key
def DECRYPTION(plaintext,  key, output_file_name):
    decryption = ''
    m = len(key)
    for i in range(len(plaintext)):
        decryption += number_to_letter[(letter_to_number[plaintext[i]] - letter_to_number[key[i % m]]) % 26]

    output_file = open(output_file_name,"w")
    output_file.write(decryption)
    output_file.close()

#index of coincidence(represents the probability that, by randomly extracting two symbols from alpha, they coincide)
#Counter-how many times does a letter apear in the alpha :{'a':10 , 'b':2 , etc}
def IC(alpha):
    index = 0.0
    frequencies = Counter(alpha)
    length = len(alpha)
    for i in frequencies:
        if length>1:
            index += (float(frequencies[i]) / length) * (float(frequencies[i] - 1) / (length - 1))
    return index

#Finding the key length using IC 
def initinal_key_length(cryptotext):
    m=0
    best_avg=0.0
    best_m=0
    ic_table=[]
    while True:
        m=m+1
        nr=0
        ic_array = list()
        for j in range(m):
            ic_array.append(IC(cryptotext[j::m]))
        average=sum(ic_array) / len(ic_array)
        #print(m," ",average ) 
        if average  > best_avg :
            best_m=m
            best_avg=average        
        if m==21:
            break    
    return best_m    


#the string obtained by replacing each symbol in alpha with s  positions in the alphabet to the right(circular)
def SHIFT(alpha, s):
    result = ''
    for c in alpha:
        if chr(ord(c) + s) > 'Z':
            c = chr((ord(c) + s) % (ord('Z') + 1) + ord('A'))
        else:
            c = chr(ord(c) + s)
        result += c
    return result

#Mutual Index of Coincidence (from 2.b.) 
def MIC_2b(beta):
    length_beta = len(beta)
    frequencies_beta = Counter(beta)
    result = 0.0
    for i in english_frequencies:
        result += english_frequencies[i] * (float(frequencies_beta[i])/ length_beta)
    return result

#Finding the key using  Mutual Index of Coincidence (from 2.b.)and choosing the bigger mic
def get_key(cryptotext,key_length):
    key=''
    for j in range(key_length):
        s=-1
        best_s= -1
        best_mic = 0
        while s<26:
            s=s+1
            mic=MIC_2b(SHIFT(cryptotext[j::key_length],s))
            if best_mic <  mic:
                best_mic=mic
                best_s=s
        c = chr((26 - best_s) % 26 + ord('A')) 
        key += c
    #print(key)
    return round_key(key)           
def round_key(key):
    divisors = []
    key_length = len(key)
    for i in range(2, int(key_length / 2 + 1)):
        if key_length % i == 0:
            divisors.append(i)
    divisors.append(key_length)
    for d in divisors:
        if key[:d] * int(key_length / d) == key:
            print("the length of the key is :",d)
            return key[:d]

def random_key():
    key=''
    n = random.randint(2,20)
    for i in range(n):
        j=random.randint(0,25)
        key+=number_to_letter[j]
    return key


Vigenere()            