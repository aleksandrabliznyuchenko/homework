The full package of all the files used during spell-checker and it's results preparation contain:
ngram_cutter.py
file_100_cutter.py
spellchecker.py

ngram_cutter.py:
Searches for dates from 16th century till 1918 and writes lines with these dates in new .txt file
The input data are unpacked files from Google Ngram Viewer
the output data are new cut files

file_100_cutter.py:
Cuts prepared in ngram_cutter.py texts so that they all would contain 100 lines or less (so that spellchecker does not fall or go mad)
The input data: cut with ngram_cutter.py texts
The output data: little texts made out of cut texts

spellchecker.py:
Firstly it takes a file with ngrams from Ruscorpora, provides each ngram with it's frequency in the file. Then reads a short file with Google ngrams, takes ngrams from every line in file, compares it with the content of the set of Ruscorpora words made previously. If an ngram is in this set, it has no mistake. Else it is edited according to 4 types of editing -- deleting a symbol, inserting a new symbol from alphabet, transpositing 2 symbols and replacing a symbol with any other from alphabet. The program may do it twice, each time it compares results with Ruscorpora set. If an edit is in Ruscorpora set, the ngram is replaced with it. If there are several variants of which edit to choose (several edits occur in the set), the most frequent one wins. If after 2 "waves" of editing there is still no match between edits and set, an ngram remains the same.
Each time the replacement is written in final file that will be modified later.
It also prints if an ngram has been edited or not

The input data: short files with ngrams, name of the folder out of which these files are taken. It's necessary because the 1st symbol of folder's name is a number (2, 3, 4 or 5, depending on the type of ngrams). It will later be used for opening the required Ruscorpora file and for defining ngrams in every line (using indexes in range 2, 3, 4 or 5)

The output data: the final file with edited lines from processed files

Drawbacks: can only edit an ngram twice -- it does not cover all the mistakes. Writes lines in one big file without alphabet sorting, each line is repeated because each time only 1 ngram is being changed. That will be later modified with another program.
