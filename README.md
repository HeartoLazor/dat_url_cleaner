# Dat URL Cleaner
Clean a list of urls using a Rom management Dat file.

## Requirements

* [Python 3.x](https://www.python.org/downloads/)

## Installation

Simply run `pip install .` from the root directory to install this package, don't forget administrator privileges. Then you can invoke it anywhere like this `python -m dat_url_cleaner -i <url_file.txt> -d <dat_file.dat> -o <result_file_name>`

## Uninstall

Run with administrator privileges `pip uninstall dat_url_cleaner`

## Usage

Dat Url Cleaner utility, cleans an url list based in a rom dat file. Useful to clean an url list that are expensive to download/store, for example playstation 1 romsets.
An example is to copy the html table from myrient download lists, use a word processor tool like sublime to leave only one link per each line and then pass that list in this tool using a dat file. Then use the generated list file in a mass downloader like jdownloader to download them all.
Generates three files after finish:
* out.txt: name can be defined by the -o command, it's the url list ready to copy to a mass downloader client like jdownloader.
* missing_file_list.log: a list of the files from the dat that has not be found in the url_list. This means that you need to look for those remaining urls to complete the dat set.
* removed_url_list.log: informative log with all of the rejected urls.
Note 1: the links requires to have the same rom/iso name as the name found in the dat file. For example if in the dat the filename is `Super Mario: Lost Levels` and in the url is `Super Mario Lost Levels`, the url will be discarded because of the `:` character. 
Note 2: the links urls can have html encoded characters, for example `Super%20Mario%20World` is transformed automatically to spaces, also caps are ignored in comparisons.

## Url List Creation Example

* Let's take myrient as an example, you go to the page with the links you want to generate a list, for example any of no-intro dumps.
* Inspect the page (F12) and pick any row and copy all the table to a word processor, we will use sublime for this example.
* Clean the html code, leaving only the table rows, which are lines enclosed by `<td>`. You will end with something like this:
  ![step_1](https://github.com/HeartoLazor/dat_url_cleaner/blob/main/readme_images/url_generation_1.png)
* Replace the left side of the url: `<tr><td class="link"><a href="` with the url to the file, for example: `https://awesome_site.com/files/Redump/Sony%20-%20PlayStation/`, you should end with something like this:
  ![step_2](https://github.com/HeartoLazor/dat_url_cleaner/blob/main/readme_images/url_generation_2.png)
* The right side is not the same for each line, for example:
  `" title="'98 Koushien (Japan) (Demo).zip">'98 Koushien (Japan) (Demo).zip</a></td><td class="size">175.9 MiB</td><td class="date">03-Apr-2024 20:43</td></tr>`
  For this reason, to remove the right side we should use regex, you can use this regex to achieve this: `\start_character[^end_character]*\end_character`, where we replace the start_character with the first character to search between and end_character with the latest character to search between, don't forget to enable regex in the sublime replace menu.
  In this example the resulted regex is start from `"` character to `break line` character, which result in
```
\"[^
]*\

```
and replace it with just a `break line`. Ending with an url list, ready to be cleaned by dat_url_cleaner:
  ![step_3](https://github.com/HeartoLazor/dat_url_cleaner/blob/main/readme_images/url_generation_3.png)

## Command list:

`-i --input_url_list`: rom input url list, where each url is one line.

`-d --input_dat`: rom organization dat file.

`-o --out`: optional parameter, cleaned generated list intended to use in jdownloader or another mass downloader client.

Example:

`python -m dat_url_cleaner -i .\example\example_urls.txt -d .\example\example_dat.dat -o .\example\example_out.dat`

You can run/edit the run_example.bat to check how the utility works, using the included example url list and dat file. 

### License

MIT License
