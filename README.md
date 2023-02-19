# map builder

Map builder is a module to create map with markers of movies of certin year, which are located closest to a certain point

## Usage

Enter required arguments into the comand line

```python
python3 /Users/julia/Desktop/OP/week_1/map/lab1_2.py 2014 49.83826 24.02324 'path to file with films'
```

## Example of file to get info from

![My Image](images/Screenshot%202023-02-19%20at%208.25.50%20PM%201.png)

## Fuctional

In the module functions are called through argparse, using comandline.

![func read file](images/carbon.png)

Function to read data from file

![func find coords](images/carbon1.png)

Function gets list of locations and returns their coordinates

![func calc distance](images/carbon2.png)

Function to calculate distance from your location to place, where movie was filmed

![func build map](images/carbon3.png)

Function to build map with 3 layers and a minimap:    
    - the map itself
    - markers
    - circle marcers

![function main](images/carbon%20(1).png)

The main body of module with argument parser

## Contributing

Any improvements are very welcomed!

## License

[MIT](https://choosealicense.com/licenses/mit/)