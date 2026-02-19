# Declaring a list literal without a comma between elements.
x = ["a" "b"]  # [implicit-str-concat]

# Using a context handler without a comma separating the arguments.
with open("hello.txt" "r") as f:  # [implicit-str-concat]
    print(f.read())
