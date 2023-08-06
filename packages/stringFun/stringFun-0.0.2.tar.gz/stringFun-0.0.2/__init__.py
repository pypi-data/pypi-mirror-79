def reverse(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    return string[::-1]


def split_without_separator(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    li=[a for a in string]
    return li


def reverse_case(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    newString=''
    for i in string:
        if i.islower():
            i=i.upper()
            newString+=i
        else:
            i=i.lower()
            newString+=i
    return newString

def stringSort(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    li=sorted(string)
    return ''.join(li)


def isPalindrome(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    return string==string[::-1]
    

def containsAnyNumeric(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    li=['1','2','3','4','5','6','7','8','9','0']
    for a in string:
        if a in li:
            return True
    return False


def containsAnyUpper(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    for i in string:
        if i.isupper():
            return True
    else:
        return False


def containsAnyLower(string):
    if not isinstance(string,str):
        raise TypeError('Please pass String object only as input.')
    for i in string:
        if i.islower():
            return True
    else:
        return False
