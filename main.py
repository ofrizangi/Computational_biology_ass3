import math
import random
import sys
import matplotlib.pyplot as plt
import pygame

alpha = 0.5
neighbors_level_percent = {
    0: 1,
    1: 1 / 2,
    2: 1 / 4
}


def draw_hexagon(surface, color, x, y, width):
    # drawing a single hex in the grid
    pts = []
    for i in range(6):
        x = x + 20 * math.cos(math.pi / 6 + math.pi * 2 * i / 6)
        y = y + 20 * math.sin(math.pi / 6 + math.pi * 2 * i / 6)
        pts.append([int(x), int(y)])
    pygame.draw.polygon(surface, color, pts, width)


# reading all the inputs from the file
def get_all_inputs(file):
    cities_and_economy = {}
    all_votes_dict = {}
    f = open(file, "r")
    f.readline()
    votes = f.readline()
    # reading line by line the file
    while votes != '':
        my_vote_list = votes.split(",")
        key = my_vote_list[0]
        my_vote_list.remove(my_vote_list[0])
        my_vote_list = [int(i) for i in my_vote_list]
        all_votes_dict.update({key: my_vote_list})
        cities_and_economy.update({key: my_vote_list[1]})
        # read another line from file
        votes = f.readline()
    f.close()
    return all_votes_dict, cities_and_economy


# choosing s vector to each position
def randomly_generate_vectors_to_each_position():
    # mapping from cell place to a vector
    vectors_dict = {}
    count = 4
    for row in range(1, 10):
        for col in range(1, 10 - count):
            vectors_dict.update({(row, col): []})
            economic = random.randint(1, 9)
            vectors_dict[(row, col)].append(economic)
            for i in range(14):
                random_vote = random.randint(1, 5000)
                vectors_dict[(row, col)].append(random_vote)

        if row < 5:
            count -= 1
        else:
            count += 1
    return vectors_dict


# find the candidate in the grid
def find_closest_vector(input_list, all_vectors_dict):
    closest_vector_place = (0, 0)
    min_difference_sum = sys.maxsize
    # finding the closest vector to the input vector
    for key in all_vectors_dict:
        my_list = all_vectors_dict[key]
        sum = 0
        for i in range(0, len(my_list)):
            sum = sum + math.pow(input_list[i] - my_list[i], 2)
        sum = math.sqrt(sum)
        if sum < min_difference_sum:
            min_difference_sum = sum
            closest_vector_place = key
    return closest_vector_place


# going over all the inputs, finding the closest vector and after that updating the input
def go_over_all_inputs_and_find_closest_vector(all_inputs, all_vectors_dict):
    closest_vectors = {}
    # go over all inputs
    for key in all_inputs:
        place = find_closest_vector(all_inputs[key], all_vectors_dict)
        if place not in closest_vectors:
            closest_vectors[place] = [key]
        else:
            closest_vectors[place].append(key)
        correct_vector_and_neighbors(all_inputs[key], all_vectors_dict, place)
    return closest_vectors


# the function for correcting the vector a specific cell
def correct_vector_values(vector, input_vector, neighbor_level):
    for i in range(len(vector)):
        vector[i] = int(vector[i] + alpha * neighbors_level_percent[neighbor_level] * (input_vector[i] - vector[i]))


def correct_vector_and_neighbors(input_vector, all_vectors_dict, place):
    correct_vector_values(all_vectors_dict[place], input_vector, 0)
    # update neighbors
    # the neighbors places change by the position of the candidate in the grid
    if place[0] == 5:
        neighbors = [(place[0] - 1, place[1] - 1), (place[0] - 1, place[1]), (place[0], place[1] - 1),
                     (place[0], place[1] + 1), (place[0] + 1, place[1] - 1), (place[0] + 1, place[1])]
        neighbors_of_neighbors = [(place[0] - 2, place[1] - 2), (place[0] - 2, place[1] - 1),
                                  (place[0] - 2, place[1]), (place[0] - 1, place[1] - 2), (place[0] - 1, place[1] + 1),
                                  (place[0], place[1] - 2), (place[0], place[1] + 2), (place[0] + 1, place[1] - 2),
                                  (place[0] + 1, place[1] + 1), (place[0] + 2, place[1] - 2),
                                  (place[0] + 2, place[1] - 1), (place[0] + 2, place[1])]
    elif place[0] < 5:
        neighbors = [(place[0] - 1, place[1] - 1), (place[0] - 1, place[1]), (place[0], place[1] - 1),
                     (place[0], place[1] + 1), (place[0] + 1, place[1]), (place[0] + 1, place[1] + 1)]
        neighbors_of_neighbors = [(place[0] - 2, place[1] - 2), (place[0] - 2, place[1] - 1),
                                  (place[0] - 2, place[1]), (place[0] - 1, place[1] - 2), (place[0] - 1, place[1] + 1),
                                  (place[0], place[1] - 2), (place[0], place[1] + 2), (place[0] + 1, place[1] - 1),
                                  (place[0] + 2, place[1] + 1), (place[0] + 2, place[1] - 1),
                                  (place[0] + 2, place[1]), (place[0] + 2, place[1] + 1)]
    else:
        neighbors = [(place[0] - 1, place[1]), (place[0] - 1, place[1] + 1), (place[0], place[1] - 1),
                     (place[0], place[1] + 1), (place[0] + 1, place[1] - 1), (place[0] + 1, place[1])]
        neighbors_of_neighbors = [(place[0] - 2, place[1] - 1), (place[0] - 2, place[1]),
                                  (place[0] - 2, place[1] + 1), (place[0] - 1, place[1] - 1),
                                  (place[0] - 1, place[1] + 2),
                                  (place[0], place[1] - 2), (place[0], place[1] + 2), (place[0] + 1, place[1] - 2),
                                  (place[0] + 1, place[1] + 1), (place[0] + 2, place[1] - 2),
                                  (place[0] + 2, place[1] - 1), (place[0] + 2, place[1])]

    # updating the neighbors
    for neighbor in neighbors:
        if neighbor in all_vectors_dict.keys():
            correct_vector_values(all_vectors_dict[neighbor], input_vector, 1)
    # updating the neighbors of neighbors
    for neighbor in neighbors_of_neighbors:
        if neighbor in all_vectors_dict.keys():
            correct_vector_values(all_vectors_dict[neighbor], input_vector, 2)


# mapping the economy average to a color by a function
def from_economy_average_to_color(closest_vector, all_input):
    place_to_rgb_dict = {}
    for place in closest_vector:
        sum = 0
        for city in closest_vector[place]:
            sum = sum + all_input[city][0]
        average = sum / len(closest_vector[place])
        # calculating the rgb color
        rgb = int((255 * average) / 10)
        place_to_rgb_dict[place] = rgb
    return place_to_rgb_dict


def draw_hub(my_screen, place_to_rgb):
    # draw the hub
    count = 4
    position_x = 170
    start_position_x = position_x
    position_y = 80
    for row in range(1, 10):

        for hex in range(1, 10 - count):
            if (row, hex) not in place_to_rgb:
                rgb = 255
            else:
                rgb = place_to_rgb[(row, hex)]
            draw_hexagon(my_screen, (rgb, rgb, rgb), position_x, position_y, 0)
            draw_hexagon(my_screen, (0, 0, 0), position_x, position_y, 1)
            position_x = position_x + 36

        if row < 5:
            count -= 1
            start_position_x = start_position_x - 18
        else:
            count += 1
            start_position_x = start_position_x + 18
        position_y = position_y + 32
        position_x = start_position_x


# print all the cities and the place in grid they are mapped to
def print_output(dict_cities):
    count = 4
    count_cell = 1
    # go over hex and print cities
    for row in range(1, 10):
        for hex in range(1, 10 - count):
            if (row, hex) in dict_cities.keys():
                for city in dict_cities[(row, hex)]:
                    print(city + " is mapped to cell " + str(count_cell) + " in grid")
            count_cell += 1

        if row < 5:
            count -= 1
        else:
            count += 1


# claculating the distance by RMS
def calculate_distance(vector1, vector2):
    sum = 0
    for i in range(0, len(vector1)):
        sum = sum + math.pow(vector1[i] - vector2[i], 2)
    return math.sqrt(sum)


# finding the number of this cell in grid by its position
def calculate_cell_number(key):
    amount = 5
    sum = 0
    for i in range(1, key[0]):
        sum = sum + amount
        if i < 5:
            amount = amount + 1
        else:
            amount = amount - 1
    sum = sum + key[1]
    return sum


def num_of_distance(len):
    sum = 0
    for i in range(1, len):
        sum = sum + i
    return sum


# claculate the maximum distance between 2 vectors mapped to the same cell
def calculate_solution_result(closest_vec, input_dict):
    list_of_max_distance = []
    list_of_keys = []
    for key in closest_vec:
        list_of_keys.append(calculate_cell_number(key))
        place_cities = closest_vec[key]
        sum = 0
        # going over
        if len(place_cities) == 1:
            list_of_max_distance.append(0)
        else:
            for i in range(0, len(place_cities)):
                for j in range(i + 1, len(place_cities)):
                    sum = sum + calculate_distance(input_dict[place_cities[i]], input_dict[place_cities[j]])
            list_of_max_distance.append((sum / num_of_distance(len(place_cities)))/10)

    return list_of_max_distance, list_of_keys


# the best result graph
def show_graph(list_of_max_distance, list_of_keys):
    # the 2 lists for the graph
    plt.bar(list_of_keys, list_of_max_distance, color='maroon')
    plt.xlabel("places in grid")
    plt.ylabel("maximum distance")
    plt.title("graph")
    plt.show()


# getting a dict sorted by total votes
def get_sorted_input_dict(input_dict, city_dict):
    sorted_list = sorted(city_dict, key=city_dict.get)
    new_dict = {}
    for key in sorted_list:
        new_dict[key] = input_dict[key]
    return new_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = "Elec_24.csv"
    input_dict, cities_and_economy = get_all_inputs(file)
    sorted_dict = get_sorted_input_dict(input_dict, cities_and_economy)
    vectors_dict = randomly_generate_vectors_to_each_position()
    closest_vectors = {}

    save_best_solution_lists = []
    save_best_solution_closest_vectors = {}
    min = sys.maxsize

    # doing 10 rounds and at each round doing 30 epocs
    for j in range(0, 5):
        for i in range(0, 30):
            closest_vectors = go_over_all_inputs_and_find_closest_vector(input_dict, vectors_dict)
        list_of_max_distance, list_of_keys = calculate_solution_result(closest_vectors, input_dict)
        # checking if this is the best solution
        if sum(list_of_max_distance) < min:
            min = sum(list_of_max_distance)
            save_best_solution_lists = [list_of_keys, list_of_max_distance]
            save_best_solution_closest_vectors = closest_vectors

    pygame.init()

    print_output(save_best_solution_closest_vectors)

    # Set up the drawing window
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                show_graph(save_best_solution_lists[1], save_best_solution_lists[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    show_graph(save_best_solution_lists[1], save_best_solution_lists[0])

        # Fill the background with white
        screen.fill((255, 255, 255))
        place_to_rgb = from_economy_average_to_color(save_best_solution_closest_vectors, input_dict)
        draw_hub(screen, place_to_rgb)

        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
