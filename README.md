# HKUST VisLab Coding Challenge

The challenges are very interesting, and they make me reflect on my skills, which inspired me to think of a more structural approach to deal with visualisation tools and data anaysis tools. I tried minimum dependency in this challenge, all the challenges are completed in python together with Numpy, Pandas and Matplotlib if it is not reuqired specifically.

## Level 1 & 2

I used different approaches to complete level1 and level2 seperately, but the idea behind them is basically the same which is to find the relation between mouse coordination and temperature record.

The visulisation method I choose was to find the highest/lowest temperature during a month in the max/min temperature records.

Note that level1 would require seaborn to run and level2 might be a little bit slow to switch due to large number of axes to render.

## Level 3

I didn't complete all the required features in level3. It could be perfectly accomplished if I know how to calculate force layout. Instead, I used a random layout here but obviously it is not a good idea since some nodes may overlapping.

However, I have implemented the basic ideas in my code which is to find a mapping function between node and its coordination in the adjacency matrix and vice versa.

## Level 4

All basic requirements are completed.

## Level 5

Level5 task is a basic image classification problem with 2 categories. I have a coursework report for image classification which discussed the relationship between performance, depth and number of labels. The report with its code is attached in this repository and they are renamed as level5.