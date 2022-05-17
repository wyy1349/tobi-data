# tobi-data
code and sample data for parsing textgrid files
(project from my UROP at MIT)
audio files and labeled textgrids not included, as they reveal too much information

What it does:
Given textgrid files, it parses and counts total occurrences of each label in each tier.
It also counts cues conditional on certain labels. (see how to specify parameters in How to Use)

How to use:
Install the relevant packages
textgrid.py contains critical modifications by me, so you should download it along with data_processing.py, under the same directory
Place the textgrid files to be processed under the same directory as data_processing. Create a directory "figs" under the same directory
If you want to count cues conditional on certain tones and breaks, replace the value of boundary_tones with the tones you care about and rename this variable accordingly; likewise, replace the value of all_breaks; if you only want to count certain cues, replace the value of relevant_cues.
When you run the file, the .txt data files will print the python dictionaries of counts; graphs will be generated under "figs"

Potential Issues:
You might find uncertain labels (the ones with ? or \*) throwing errors. I did not use many uncertain labels, so I did not include code to process them for every tier. However, I have some code that handles that already in data_processing.py, and you can adapt them for the functions that are missing this. 
