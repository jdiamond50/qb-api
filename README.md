# qb-api

A project to explore the functionality of APIs using the QBReader database by compiling a packet of tossups to be read aloud via text-to-speech.

# Running the Program
Create a packet with `make packet`. You will be prompted for the difficulties, categories, and number of questions.
Run the question reader with `make reader`.

## Flags
Flags may be used to change the output of the program. Add flags using `make packet ARGS="<flags>`\
&emsp;**-v** or **--verbose** &emsp;&emsp; enables verbose mode\
&emsp;**-s** or **--slow** &emsp;&emsp;&emsp;&ensp;&nbsp; enables slow reading mode
