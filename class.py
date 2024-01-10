class NumberManager:

    def __init__(self, num_list):
        self.num_list = num_list #the list to be processed 
        self.num_count_pairs = {}
        self.most_common = -1

    def find_occurrences(self):
        for number in self.num_list:
            if (number in self.num_count_pairs):  #Number exists in dict already
                self.num_count_pairs[number] += 1
            else:    #First occurrence of number
                self.num_count_pairs[number] = 1
        print("Occurrences of each number in list: ", self.num_count_pairs)

    def most_common_item(self):
        highest = 0
        most_common = []
        for number, occurrences in self.num_count_pairs.items():
            if occurrences > highest:
                most_common = [number]
                highest = occurrences
            elif occurrences == highest:
                most_common.append(number)

        print("Most common item(s):", most_common)

#Testing
number_manager = NumberManager([1,2,2,3,2,4,3])
number_manager.find_occurrences()
number_manager.most_common_item()