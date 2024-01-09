def find_occurrences(numbers):

    #Creating a dictionary to store number and its occurrences as key value pair:
    num_count_pairs = {} 
    for number in numbers:
        if (number in num_count_pairs):  #Number exists in dict already
            num_count_pairs[number] += 1
        else:    #First occurrence of number
            num_count_pairs[number] = 1
    print("Occurrences of each number in list: ", num_count_pairs)

#Test cases
example1 = [
    1 , 1, 4, 
    4, 6, 32, 
    32, 32, 5, 
    522, 0,
    ]
example2 = [
    24 , 3, 5, 
    5, 6, 11, 
    11, 32, 5, 
    5, 52, 32, 
    0, -4,
    ]
example3 = []   
find_occurrences(example1)
find_occurrences(example2)
find_occurrences(example3)


 