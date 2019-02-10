# Tv Series Graphs
It is a simple script/program that lets you create graphs from ratings and the number of votes for a specific tv series. Currently the only supported site is IMDb, however I build it with scalability in mind and it is very easy to get a new source of data.

## Installation
Currently the only way to install my program/script is manually downloading it from github, support for `pip` will be added.

#### Requirements
* Python 3.x
* [Bokeh](https://bokeh.pydata.org/en/latest/) library 
```
pip install bokeh
```
* [IMDbPY](https://github.com/alberanid/imdbpy) library 
```
pip install imdbpy
```

## Usage
To run the script you have to pass these obligatory arguments:
* `--id`/`-i` - ID of the show from IMDb site. To get the ID all you have to do is go on an IMDb website, choose a show and the ID will be in a link. For example, here is a link to the Game Of Thrones, `https://www.imdb.com/title/tt0944947/?ref_=nv_sr_1`, the ID is the number after `/tt`, in this case it is `0944947`.
* `--link`/`-l` - Instead of the ID of a show you can pass a link after this flag and the script will retrive the ID for you.

    **Make sure that both link and ID are referring to the entire show, not a single episode** 

* `--data`/`-d` - What type of data you want to display, currently only two types are supported, the number of votes per episode and ratings. You can pass 'r' to display only ratings, 'v' for votes or 'rv' to see both on one graph (can be very interesting sometimes, when death of a single character drastically influences the ratings and number of votes)

You can also add optional arguments:
* `--file`/`-f` - If you have previously run the script for a show and marked to save the data, you don't have to run it again. With this flag the script will search for the data in its directory.
* `--save`/`-s` - With this flag you can save downloaded data for future use.
* `--normalize`/`-n` - If you want to normalize data to be in range 0-10, set as default when displaying both ratings and number of votes together because you can barely see ratings without it.
* `--average`/`-a` - If you want to display a line that will show you the average rating/number of votes for a show.
* `--seasons START:END` - You can filter particular seasons from a tv series. START is starting seasons and END is the last seasons that you want to show, every season in that range will be displayed. If you want to show only one season assign the same value to both variables. 
NOTE: This won't prevent the script from downloading data for other seasons, it will just filter displayed data.


You can also always run the script with `-h` or `--help` flags to get quick info about all available options.

## Example usage
Running:
```
python Show_Graphs.py -l https://www.imdb.com/title/tt0475784/?ref_=nv_sr_1 -a -d rv
```
You will be asked if the show name is correct:
![](https://github.com/kubapilch/Show-Details/blob/master/examples/sure.png)

Then the downloading process will start, it can take a couple of minutes, depending on your internet speed and the number of episodes
![](https://github.com/kubapilch/Show-Details/blob/master/examples/downloading.png)

After some time this graph will be opened in your browser
![](https://github.com/kubapilch/Show-Details/blob/master/examples/graph.png)

You can click on a legend to 'mute' or 'unmute' particular lines. 

## What I have learned
* How to pass arguments with `argparse`
* How to write unit tests with `unittest`
* Improved skills with `bokeh` library
* How to create text-based progress bar

## Future plans
* ~~Adding filtering seasons with `--seasons` flag~~
* ~~Refactoring code to be faster and more efficient~~
* Support for couple sites/sources
* Better exceptions handling, including:
    * ~~If only ratings/votes are saved locally, but both are needed - now you have to re-run the script to download only one data to avoid downloading both.~~
* Compare  mode that will allow user to overlap ratings from two different shows or two seasons from one show.
* Installation via `pip`
* Release .exe file of the script