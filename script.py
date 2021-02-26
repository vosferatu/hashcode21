import math
import sys
import pdb

filename = sys.argv[1]

def parse_input_file(input_name):
  file = open(filename, mode='r')
  line = file.readline()
  line_elements = line.split()
  streets = dict()
  cars = []
  duration, n_intersections, n_streets, n_cars, points_per_car = [int(elem) for elem in line_elements]

  for _ in range(n_streets):
    line = file.readline()
    line_elements = line.split()
    intersection_start, intersection_end, street_name, street_duration = line_elements
    intersection_start, intersection_end, street_duration = int(intersection_start), int(intersection_end), int(street_duration)
    streets[street_name] = {
      'start': intersection_start,
      'end': intersection_end,
      'duration': street_duration
    }

  for _ in range(n_cars):
    line = file.readline()
    line_elements = line.split()
    car_street_count = int(line_elements[0]) 
    car_path = line_elements[1:]
    cars.append(car_path)

  return duration, n_intersections, streets, cars, points_per_car


duration, n_intersections, streets, cars, points_per_car = parse_input_file(filename)
solutions = []

# Intersections that can always be green => Only 1 incoming street
incoming_street_intersections = [[] for _ in range(n_intersections)]
missing_intersections = []

for street_name,v in streets.items():
  intersection = v['end']
  incoming_street_intersections[intersection].append(street_name)

for intersection in range(n_intersections):
  street_names = incoming_street_intersections[intersection]
  if len(street_names) == 1: #TODO: eliminate useless streets
    solution = {
      'intersection': intersection,
      'streets': [ {'name': street_names[0], 'duration': 1} ]
    }
    solutions.append(solution)
  else:
    missing_intersections.append(intersection)

# histogram = [{str_name: 0 for str_name in streets.keys()} for _ in range(duration)]
histogram = {str_name: [0 for _ in range(duration) ] for str_name in streets.keys() }

for time in range(duration):
  for car in cars:
    total = 0
    index = 0
    for car_str_name in car:
      total += streets[car_str_name]['duration']
      if total >= time:
        break
      else:
        index += 1
    try:
      car_current_street = car[index]
    except IndexError:
      car_current_street = car[index - 1]
    histogram[car_current_street][time] += 1



for intersection in missing_intersections:
  incoming_streets = incoming_street_intersections[intersection]
  street_averages = list()

  for street in incoming_streets:
    distribution = histogram[street]
    avg = sum(distribution) / duration
    street_averages.append({ 'name': street, 'avg': avg})

  sorted_sa = sorted(street_averages, key=lambda x: x['avg'])
  minimum = next((i for i, x in enumerate(sorted_sa) if x['avg'] > 0), 0)
  minimum = sorted_sa[int(minimum)]['avg']
  sols = []
  tmp = 0

  if minimum < 1:
    tmp = 1
  else:
    tmp = math.floor(minimum)
  
  for elem in sorted_sa:
    avg = elem['avg']
    ratio = avg / tmp
    seconds = math.floor(ratio * tmp)
    if seconds > duration:
      seconds = duration
    elif seconds < 1:
      seconds = 1
    sols.append({'duration': seconds, 'name': elem['name'] })
    
  solutions.append({
    'intersection': intersection,
    'streets': sols
  })

file = open('output/' + filename, mode='w')
file.write(str(len(solutions))+'\n')
for sol in solutions:
  file.write(str(sol['intersection'])+'\n')
  file.write(str(len(sol['streets']))+'\n')
  for s in sol['streets']:
    file.write(s['name'] + ' ' + str(s['duration'])+'\n')
  





