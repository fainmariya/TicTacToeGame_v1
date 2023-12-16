largest_number = -999999999
number = int(input("Enter number: "))
if number == -1:
    print(largest_number)

if number > largest_number:
    largest_number = number
    print(largest_number)
# Go to line 02