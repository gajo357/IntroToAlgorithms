import unittest

def importance_rank(items, weights):
    names = [item[0] for item in items]  # get the list of animal names
    scores = [sum([a*b for (a,b) in zip(item[1:], weights)]) for item in items]  # get the list of overall scores for each animal
    results = zip(scores,names) # make a list of tuple
    res2 = sorted(results) # sort the tuple based on the score
    return res2

def second_most_popular_female_name(lines):
    most_popular_count = None
    most_popular = None
    second_most_popular = None
    second_most_popular_count = None

    for line in lines:
        (name, sex, count) = line.rsplit(',')
        if(sex == 'M'): 
            continue
        
        name_count = int(count)
        if most_popular_count == None or most_popular_count < name_count:
            second_most_popular_count = most_popular_count
            most_popular_count  = name_count

            second_most_popular = most_popular
            most_popular = name
        elif second_most_popular_count == None or second_most_popular_count < name_count:
            second_most_popular_count = name_count
            second_most_popular = name
    return second_most_popular

class test_lesson(unittest.TestCase):
    def test_names(self):
        with open('namesUs1995.txt') as f:
            lines = [line.rstrip('\n') for line in f]
        self.assertEqual(second_most_popular_female_name(lines), 'Ashley')

    def test_animals(self):
        #            animal       speed   weight lifespan brain
        #                          (mph)   (kg)  (years) mass (g)
        animals = [("dog",          46,   35,     13,  280    ),
                   ("elephant",     30, 3500,     50, 6250    ),
                   ("frog",          5,    0.5,    8,    3    ),
                   ("hippopotamus", 45, 1600,     45,  573    ),
                   ("horse",        40,  385,     30, 642     ),
                   ("human",        27,   80,     78, 2000    ),
                   ("lion",         50,  250,     30,  454    ),
                   ("mouse",         8,    0.025,  2,    0.625),
                   ("rabbit",       25,    4,     12,   40    ), 
                   ("shark",        26,  230,     20,   92    ),
                   ("sparrow",      16,    0.024,  7,    2    )]
        answer = importance_rank(animals, (2,3,7,1))
        self.assertEqual(answer[3][1], 'rabbit')
