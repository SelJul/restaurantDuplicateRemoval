# RestaurantDuplicateRemoval

This is a university project about removing duplicate restaurant data from a TSV file. 
Three different methods will be used to remove as many duplicates as possible. 
At the end every method will be evaluated based on the gold standard regarding 
precision, recall and F1 Score.

The restaurant data set and the gold standard are provided by the Hasso-Plattner-Institut: 
https://hpi.de/naumann/projects/repeatability/datasets/restaurants-dataset.html

## Notes before starting

Some of the functions are commented out. These include functions that print all street types,
phone formats, etc. These were functions that helped in the auditing decisions. 
If someone is to see the reason why some of the mapping was decided
how it is currently, the code has to simply be uncommented. 


There is also a function to load the data into a MongoDB Atlas cluster. However, mongoimport 
is needed for for that. The function uses the command line to import the data into the db. 
These can not be viewed, but the success or failure will be logged.


### Prerequisites MonogDB

```
mongoimport
```
### Atlas cluster

The atlas cluster will only remain active for one week in the free tier. So, after one week it becomes unavailable.

### Python version
The python version that was used throughout the whole project was 3.7.
## Running the code

To run this code use the main.py. The other files fmt_methods.py and restaurant_audit.py are also
necessary but are imported in the main.py. The code will run and show the precision, recall
and F1 Score from each methods.

The fmt_methods.py contains all the field matching techniques that were used.

The restaurant_audit.py contains all code that has to do with the auditing.

The test_fmt_methods.py was used to test the methods from the fmt_methods.py file.


## Author

**Julian Sellner** 

