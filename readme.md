# Friends OMG

We were rewatching some old Friends episodes at home when I took notice that the phrase _"oh my god"_
comes up a lot in that show. As any reasonable person would, I compiled script data and built a website to
prove my point.

This webapp lets you check how often phrases like "oh my god" are said in Friends, Seinfeld, 
and Sex and the City.

## Building the Dataset

I tried to make the data build as self-contained as possible. To that end I have hosted some source files on my personal heliohosting server. There are two unrecoverable aspects to the data:

1. The source seinfeld data is no longer available online. [Colin](https://github.com/colinpollock) sent a copy to me, and thats how i have it.
2. The Sex and the City data were messy in their public form (via Kaggle). I cleaned those data up a fair amount and saved the file.

The [download-all](bin/download-all) script contains relevant URLs to download the source data used tobuild the final dataset. After downloading those raw files, the [build](build/) module contains code to process the files in their raw form in order to prodice a final dataset.

You can download a copy of it [here](http://nolanc.heliohost.org/omg-data/data.db)!


### Data Credits

I did basically zero work obtaining the source data. Below are shout-outs to those who did that hard work:

1. [Colin Pollock](https://github.com/colinpollock/seinfeld-scripts) for the _excellent_ Seinfeld dataset.
2. [Yusuf Sohoye](https://quotennial.github.io/Friends-engineering) for the regex to parse through Friends script files. 
3. I stole the Sex and the City data from [Kaggle](https://www.kaggle.com/snapcrack/every-sex-and-the-city-script).

You can download my the full (gzipped) SQLite3 database [here](http://nolanc.heliohost.org/omg-data/data.db)!
