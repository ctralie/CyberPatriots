from sys import argv
import time
import itertools
import numpy as np
import time

def guess_password_generators(passwd, chars, password_length):
    attempts = 0
    for guess in itertools.product(chars, repeat=password_length):
        attempts += 1
        guess = ''.join(guess)
        if guess == passwd:
            return(True, attempts)
    return (False, attempts)

def containedin(passwd, chars):
    """
    See if all of the characters in the password are contained
    in this list of chars
    """
    for p in passwd:
        if not p in chars:
            return False
    return True

def guess_password(passwd, skipsimulation = False):
    lowercase = [chr(ord('a') + i) for i in range(26)]
    uppercase = [chr(ord('A') + i) for i in range(26)]
    numeric = ["%i"%i for i in range(10)]
    upperlower = lowercase + uppercase
    alphanum = lowercase + uppercase + numeric
    attempts = 0
    fin = open("words.txt")
    print("Looking in dictionary")
    dictwords = [s.strip() for s in fin.readlines()]
    fin.close()
    for s in [dictwords[i] for i in np.random.permutation(len(dictwords))]:
        attempts += 1
        if s == passwd:
            print("Found password after %i attempts"%attempts)
            return
    
    print("Looking in names")
    fin = open("names.txt")
    names = [s.strip() for s in fin.readlines()]
    for s in [names[i] for i in np.random.permutation(len(names))]:
        attempts += 1
        if s == passwd:
            print("Found password after %i attempts"%attempts)
            return
        attempts += 1
        if s.capitalize() == passwd:
            print("Found password after %i attempts"%attempts)
            return


    for password_length in range(1, 20):
        for name, chars in zip(['numeric', 'lower case', 'upper case', 'alpha', 'alphanumeric'], [numeric, lowercase, uppercase, upperlower, alphanum]):
            print("Trying all %s combinations on passwords of length %i"%(name, password_length))
            if skipsimulation:
                n_combos = len(chars)**password_length
                if len(passwd) > password_length:
                    attempts += n_combos
                else:
                    if not containedin(passwd, chars):
                        attempts += n_combos
                    else:
                        attempts += int(np.random.rand()*n_combos)
                        print("Found password after %i attempts"%attempts)
                        return attempts
            else:
                charsparam = [chars[i] for i in np.random.permutation(len(chars))]
                res = guess_password_generators(passwd, charsparam, password_length)
                attempts += res[1]
                if res[0]:
                    print("Found password after %i attempts"%attempts)
                    return attempts
    print("Did not find password!!")
    return attempts



if __name__ == '__main__':
    tic = time.time()
    guess_password(argv[1], skipsimulation=True)
    print("Elapsed Time: %.3g"%(time.time()-tic))