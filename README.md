README to be expanded in the future
### Project Description
Analyze the qualities of one set of coordinates around a second set of coordinates. Throughout the program 
code and this description, coordinate set 1 is referred to as 'outposts', and coordinate set 2 are referred to as 
'scouts'. Per their names, this project concerns itself with the number, distance, qualities, and statistics of scouts 
around individual outposts. Each outpost is independent of one another, so there is no need to regard any overlap of 
outposts analysis. 

### Project Code and Implementation
The overall program is managed through the EnvironmentManager class. Initializing an EnvironmentManager class object 
is the first step when using this program. See the documentation for details. After creating the EnvironmentManager 
class object, functions can be called. Each function call adds to the function stack in an automatically generated 
FunctionStack class object.

### Class Usage
1) Instantiate an EnvironmentManager object
2) Call the desired analysis functions (e.g.: count_scouts_by_variable, nearest_scout)
3) Call function output_data_to_file
