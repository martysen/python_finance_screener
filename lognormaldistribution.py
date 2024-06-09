import math

'''
A function to compute the lognormal distribution of an input

input: value to compute. represented as lognormal_dist_input
output: computed value represented as lognormal_dist_output
'''

def compute_lognormal_dist(lognormal_dist_input):
  # print("lognormal_dist_input is {}".format(lognormal_dist_input))
  lognormal_dist_output = 0

  temporary_variable_y =  1 / (1 + (0.2316419 * abs(lognormal_dist_input)))
  # print("value of temp_variable_y is {}".format(temporary_variable_y))

  temporary_variable_z = 0.3989423 * math.exp(-((lognormal_dist_input * lognormal_dist_input)/2))
  # print("value of temp_variable_z is {}".format(temporary_variable_z))

  lognormal_dist_output = 1 - temporary_variable_z*((1.330274*math.pow(temporary_variable_y, 5)) - (1.821256 * math.pow(temporary_variable_y, 4)) + (1.781478 * math.pow(temporary_variable_y, 3)) - (0.356538 * math.pow(temporary_variable_y, 2)) + (0.3193815 * temporary_variable_y))

  # print("value of temp_variable_x is {}".format(lognormal_dist_output))

  if lognormal_dist_input > 0:
    return round(lognormal_dist_output, 5)
  else:
    return round((1 - lognormal_dist_output), 5)