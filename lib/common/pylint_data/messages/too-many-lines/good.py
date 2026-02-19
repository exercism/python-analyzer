def is_palindrome(string):
    return string == string[::-1]


def main():
    for string in ["aza", "racecar", "trigger", "ogre"]: # [loop used instead of separate lines]
        print(is_palindrome(string))
