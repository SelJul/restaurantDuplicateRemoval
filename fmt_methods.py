def levenshtein(s1, s2):
    """
    Show the shortest number of operations two strings have to go trough to be the same

    Parameters
    ----------
    s1 : str
        First string
    s2 : str
        Second string

    Returns
    -------
    int
        Number of operations
    """

    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def dice_coefficient(a, b):
    """
    Check the similarity between two strings according to the dice coefficient

    Parameters
    ----------
    a : str
        First restaurant name
    b : str
        Second restaurant name

    Returns
    -------
    float
        Returns the dice coefficient of the two values
    """

    if len(a) == 0 and len(b) == 0:
        return 1.0

    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)

    sim = overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))

    return sim


def soundex(string):
    """
    Transforms a string which will be the restaurant name into their soundex-code

    Parameters
    ----------
    string : str
        Restaurant name from which the soundex codes will be made

    Returns
    -------
    str
        Returns the soundex-code of the restaurant name
    """

    string = string.lower()
    letters = [char for char in string if char.isalpha()]

    if len(string) == 1:
        return string + "000"
    # Special case were name is made from numbers hat string contains no char
    if len(letters) == 0:
        return "0000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = letters[0]
    letters = letters[1:]
    # Remove all occurrences of a, e, i, o, u, y, h, w.
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"

    # Replace all consonants with digits according to the rule

    to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    first_letter = [value if first_letter else first_letter for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]

    # Replace all adjacent same digits with one digit.
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]

    if first_letter == letters[0]:
        letters[0] = string[0]
    else:
        letters.insert(0, string[0])

    first_letter = letters[0]
    letters = letters[1:]

    # Remove all except first letter and 3 digits after it.
    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    return string
