# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/
# modified by nicb to have a start and a stop arguments

def __sieve__(last_prime):
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}
    
    # In order for the sieve to work properly you need to start from the first
    # non-trivial prime, 2
    q = 2
    # The running integer that's checked for primeness
    
    while True and (q < last_prime):
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            # 
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next 
            # multiples of its witnesses to prepare for larger
            # numbers
            # 
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1


def sieve(first_prime, last_prime):
    """ sieve(first_prime, last_prime)

        Generates a finite sequence of prime numbers, from the first prime in
        the series (first_prime) to the last one (last_prime)
    """

    l = __sieve__(last_prime)
    return [p for p in l if p >= first_prime]
