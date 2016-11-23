#!/usr/bin/python

def partition(ar, a, b) :
    j = a
    pivot = ar[b]
    for i in range(a, b) :
        if ar[i] < pivot :
            ar[i], ar[j] = ar[j], ar[i]
            j += 1
            pass
        pass
    ar[j], ar[b] = ar[b], ar[j]
    return j

def quicksort_imp(ar, a, b) :
    if a >= b : return
    p = partition(ar, a, b)
    quicksort_imp(ar, a, p - 1)
    quicksort_imp(ar, p + 1, b)
    pass

def quicksort(ar) : quicksort_imp(ar, 0, len(ar) - 1)

def sherlock_and_pairs() :
    T = int(input())
    for t in range(T) :
        N = int(input())
        ar = [int(i) for i in input().split(" ")]
        quicksort(ar)
    
        total = 0
        count = 1
        for i in range(1, N) :
            if ar[i - 1] == ar[i] : 
                count += 1
            else :
                total += count*(count - 1)
                count = 1
                pass
            pass
        total += count*(count - 1)
    
        print(total)
        pass
    pass

if __name__ == '__main__':
    sherlock_and_pairs()


