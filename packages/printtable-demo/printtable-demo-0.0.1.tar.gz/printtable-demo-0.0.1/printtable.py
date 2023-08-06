"A package for generating tables"

__version__ = "0.0.1"

def multtable(start, stop, number):
    """
    Print multiplication table for <number>
    from <start> to including <stop> 
    """
    for i in range(start, stop+1):
        print(f"{i} x {number} = {i*number}")

if __name__ == '__main__':
    multtable(1, 4, 7)
