import re

# filepath = "test_input_1.txt"
filepath = "input.txt"

sum = 0
for line in open(filepath):
    numbers = re.findall(r"(\d)", line)
    first = numbers[0]
    last = numbers[-1]
    number = int(first + last)
    sum += number

print(sum)
