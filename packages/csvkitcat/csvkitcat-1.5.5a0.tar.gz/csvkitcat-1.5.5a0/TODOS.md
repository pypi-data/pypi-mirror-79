# TODOS


## Priority

ONGOING:
- csvrgrep: 
  - [X] learned that regex module is very slow compared to re, for some reason...
  - [X] added `from csvkitcat import rxlib as re`, to all tools except for csvnorm

  - [x] pull out the csvsed grep into its own method
  - [x] basic implementation and tests
  - [x] write and test error handling
  - [X] move into csvsed
    - [?] or should I just leave it out of csvsed??
    - [X] benchmarks/fooprofile.py sed runs pretty well
  - [X] benchmark csvrgrep; is it any faster than multiple invocations of csvgrep?
    - A little bit slower somehow, but we'll worry about it later
  - [ ] move into csvxcap/find/split
  - [ ] clean up csvrgrep.filter_rows
  - [ ] To think on: is it a problem that csvrgrep doesn't have an option that effectively ORs the results of each expression? How would that even work? Other than to write a custom CSV filterer
    - [X] write a test to affirm that multiple expressions are ANDED

- csvsed: 
  - [ ] Unbroke it on 2020-09-10 with successful integration with csvrgrep.filter_rows
  - [ ] Clean up/rethink how sed_expressions are executed on each row
  - [ ] Write a helper to clean/normalize self.sed_expressions
  - [ ] Write more tests
    - [ ] Write test for complicated CSV that reflects how order of expressions can change results

```sh
time cat ZUNK/mass-fec.csv | 
  csvgrep -c 1-77 -a -r '\w{15,}' |
  csvgrep -c 1-77 -a -r '^[ADJBT]' |
  csvgrep -c 1-77 -a -r '\d{5,}' |
  csvgrep -c 1-77 -a -r 'DONALD|JOSEPH' |
  csvgrep -c 1-77 -a -r 'TRUMP|BIDEN' |
  wc -l 

real  0m5.386s
user  0m18.642s
sys 0m0.612s

time cat ZUNK/mass-fec.csv |   csvgrep -r 'BIDEN|TRUMP' -a -c 1-77 | wc -l

real  0m3.925s
user  0m3.853s
sys 0m0.113s

###################

time cat ZUNK/mass-fec.csv |
  csvrgrep -E '\w{15,}'     \
           -E '^[ADJBT]' \
           -E '\d{5,}' \
           -E 'DONALD|JOSEPH' \
           -E 'TRUMP|BIDEN' |
  wc -l 

real  0m6.356s
user  0m6.251s
sys 0m0.148s

time cat ZUNK/mass-fec.csv |   csvrgrep -E 'BIDEN|TRUMP' | wc -l
real  0m4.153s
user  0m4.037s
sys 0m0.152s

```


- csvsed: 
  - [X] change `-X` to `-G/--grep-rows/grep-match`
  - [ ] write tests for multiple invocations of `-E`
  - [ ] FilterMoreCSVReader.standardize_stuff/patterns should conver patternslist to: 
    - a dict where each key is a pattern-expression, and each value is a list of columns to test; an empty list is all columns
    - in theory, we want to iterate per sed_expression when doing pattern matching by row
      - 

  - [ ] benchmark the sloppy draft of csvsed with multi-expression searching
  - how does regular sed deal with chained expressions


In general:

- [ ] write a better csvkitutil class, with consistent implementation of init common args

- [ ] add library version info; implement similar to dannguyen/pgark https://github.com/dannguyen/pgark/blob/master/setup.py
- [ ] makes changes to `setup.py` as per above


- [ ] clean up code with Black
  - [x] some tests blacked
- [ ] consider implementing custom `_init_common_parser` common to all csvkitcat utils  


- csvsed:
  - [X] `--replace` replace entire field, e.g. 'Hello world'
  - performance:
    - debug by copying FilteredCSVReader and rewriting csvgrep
    why is:

    ```

    ```


- csvgroupby 
  - needs more documentation

- csvchart
  - [ ] assume -X/Y/C are column names. Unless `--alt` is passed in
  - [x] with no parameters, create a bar chart, with the x-column being the first Text column, and the y-column being the first Number column
  - [ ] decide whether -X, -Y, -C should take in existing column names for simplicity sake. Or should allow full altair syntax
  - [ ] -X,-Y,-C should accept things in 'Custom Axis Name|col_name:args1,args2'
  - [ ] maybe write my own extract_column_identifier function
  - [ ] labels parameter https://altair-viz.github.io/gallery/bar_chart_with_labels.html
  - [ ] add default tooltip https://altair-viz.github.io/gallery/scatter_href.html
  - use altair (since leather is in maintenance mode)
    - by default, we use altair_viewer to open the chart -- user has choice to interactively save as png
      - https://github.com/altair-viz/altair_viewer
      - import altair_viewer; altair_viewer.show(chart)
      - make option to export altair JSON, e.g. `chart.save('something.json', format="json")`
      - can't use altair_saver because of `ValueError: No enabled saver found that supports format='svg'`

    - charts
      - bar_chart: https://altair-viz.github.io/gallery/bar_chart_horizontal.html
      - column_chart: https://altair-viz.github.io/gallery/simple_bar_chart.html
      - histogram: https://altair-viz.github.io/gallery/simple_histogram.html (or do binning as csvbin?)
      - line_chart: https://altair-viz.github.io/gallery/simple_line_chart.html
        - https://altair-viz.github.io/gallery/multi_series_line.html
      - scatterplot: 


    - chartDEPRECATE
      - default: terminal bar chart
        - takes x-col and y-col
        - prints to terminal
      - SVG mode
        - [ ] by default, write to temp file and open immediately
        - [ ] if `-o` provided, write SVG to it and open immediately
        - [ ] if `-O` write to stdout, no browser
        - [ ] if `-q` be quiet, no browser

- csvslice
  - wtf is this terrible and inefficient code? `rowslice = list(myio.rows)[slice_start:slice_end]`
`  

- csvbin: https://agate.readthedocs.io/en/1.3.1/api/table.html#agate.Table.bins

- csvuniq:
  - utility to calculate ordinality
  - shortcut for `csvcut -c category | sort | uniq -c | sort -rn`
  - look at how `csvstat` and `xsv frequency` does it
  - https://agate.readthedocs.io/en/1.6.1/cookbook/filter.html#distinct-values
  
- csvround
  - for numbers, round by integer and precision
  - for dates, perform strftime
  - for text, truncate

- Content and guides
  - Real-world scenarios
    - for babynames, do a trend: csvstack, csvchart, csvpivot
    - Count crime types by year: csvround, csvpivot
    - Extract mentions from tweets by date: csvround, csvxtract (requires a util to denormalize?)
  - Tool page
    - [ ] Each description section should have a h3:Example subsection


- csvnorm
  - need flag for just minimal space-fixing, e.g. `--min/--lite`, for translit stuff

- csvrange
  - use builtin Agate examples: https://agate.readthedocs.io/en/1.6.1/cookbook/filter.html#values-within-a-range

- Categorize utils:
    - inspection: csvcount, csvflatten
    - transformation: csvnorm, csvsed, csvpad?
    - augmentation, csvxcap/xfind/xsplit, 
    - computation: csvpivot, csvchart, csvround?
    - filtering: csvslice, csvrange?





## Lesser priority/maybe deprioritize


consider usecase for integrating clevercsv: https://github.com/alan-turing-institute/CleverCSV

csvcount
- [X] change basic behavior to output rows,cells,empty_rows,empty_cells
  - [ ] Refactor the resulting spaghetti code and nested logic
-  pattern matching `-p [pattern]`
  - [X] given a list of [PATTERN], return row and column count that contain [PATTERN]
  - [X] return list of total matches, as some cells have more than one cell


csvsed

- [ ] remove boilerplate/unnecessary arguments. Should defer as much as possible to csvformat
- [ ] benchmarking....majorly slow as hell: tests/benchmark/rawsed.py
- [x] --whole option: match and replace entire field instead
  - [?] unfortunately I did it brute force dumb way and it is substantially slower than non--whole
  - [ ] sketch out usecases for whole-cell match/replace, compare to Excel


csvpad
- [ ] basic implementation and tests
    ```sh
    --left 5 '0'
    --right 
    ```


csvxplit
- [ ] advanced feature: --max-split: make the number of new split columns based on the max number of splits found. Requires basically iterating through twice...


csvflatten, csvcount
- [ ] Major revamps were done, need to come up with more robust tests to make sure all weird edgecases are covered.


csvxfind, csvxcap
- Provide option to specify prefix? 


csvpivot

- https://agate.readthedocs.io/en/1.6.1/api/table.html#agate.Table.pivot
- [ ] option to sort? But is that even useful when doing just a column pivot? How about ordering columns alphabetically/numerically too? `--sort-row` `--sort-col` `a,z,n,0`
- [ ] grand total column and row?

- Table.pivot() params to consider:
  - default_value – Value to be used for missing values in the pivot table. Defaults to Decimal(0). If performing non-mathematical aggregations you may wish to set this to None.





### Just done


- csvgroupby: csvpivot doesn't allow for multiple value calculations, e.g `SELECT country, MAX(age), MEAN(age) FROM data GROUP BY country`
  - https://agate.readthedocs.io/en/1.6.1/api/table.html#agate.Table.group_by
  - basic implementation
    - [X] needs more tests
    - [X] defaults to `Count()`; `-a/--aggs` needs to parse multiple functions, e.g. `--agg "Optional column name|sum:age`
    - [X] do ColumnIdentifierError when attempting to aggregate invalid column name

- csvpivot: fixing how --agg works and is delimited:
  - [x] `--agg sum:age` instead of `--agg sum,age`
  - [x] `--agg list` to get list of stuff

csvpivot
- [x] basic implementation and tests
  - [x] the `-r` param takes in multiple comma-delimited fields
- [x] default counting behavior
- [x] add support for other aggregations


csvflatten
- [X] Independently handle newlines

csvxplit
- [X] basic implementation and testing

csvxcap
- like csvxplit, except creates columns based on captured groups
- [x] basic implementation

csvxtract/xfind
- ???: does a regex.findall, and group concats them into a column?
- [x] basic implementation

-----------------------

## on deck/non-priority

## csvslice
  - [ ] csvhead: basically a reskin of csvslice
  - [ ] csvtail: not trivial, will need to research this
  - read up on csvkit followup issue: https://github.com/wireservice/csvkit/issues/669


## in general

- [x] rename csvkitcat.utils_plus to moreutils
- [ ] how should i deal with `override_flags`?
- [ ] extract/abstract boilerplate csvwriter args stuff, via csvflatten and csvsed
- [ ] add skip-line functionality to csvsqueeze, slice, etc
- [ ] print out separate version number

## csvcount

- [ ] kill unnecessary arguments
  - [?] partially did this by looking at `csvkit.cli._init_common_parser(self)`
  - [x] added custom `_extract_csv_reader_kwargs` to alltext.py, with a third argument to `getattr` to prevent error

- [ ] copy https://csvkit.readthedocs.io/en/latest/scripts/csvstat.html
    ```py
            if self.args.count_only:
            count = len(list(agate.csv.reader(self.skip_lines(), **self.reader_kwargs)))

            if not self.args.no_header_row:
                count -= 1

            self.output_file.write('Row count: %i\n' % count)

            return
    ```
- [x] basic implemention
- [x] edge cases with negative start/end
- [x] basic error cases

## csvflatten

- `--row-id` add row_id column (line number?)
- chop new rows for every new line? (make new test file)
- any need to remove unnecessary arguments from base CSVKitUtility?
- csvflatten should have inference
- how does typecasted values work?
- make sure 2.x and 3.x compatible

- [X] write tests
- [x] why do I have to set quote mode to 1 when working with examples/longvals.csv?
- [na] add flag to do max-length record breaking, but in newline mode (e.g. ideal for spreadsheets)
    - Don't need this because in spreadsheets, users can format column width vidsually


## csvsqueeze

- implement by character stripping
    - pass args to lstrip, rstrip










------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
# DRAFT STUFF/dumb ideas

## csvheaders

- get list
- create
- rename
- mute/omit



## csvblob


output record_id,record

```
  
  [[rowid]]
  1  

  [[date]]
        
  [[name]]
  
  [[whatever]]

```




## csvreplace

like `csvsed`, except replaces entire column

```
--columns
--pattern
--output '$1'
```


### csvfind (already done by csvcount)

- for every row, count number of matches with given pattern
- create column with find_count
- create column with find_extracts: line for every match




## old todos


csvsqueeze->csvnorm

- [X] pass newly refactored tests
- [?] refactor csvsqueeze because it looks like spaghetti barf
    - [ ] mostly did this
- [X] add norm-casing
- add toggle type options? https://stackoverflow.com/questions/34735831/python-argparse-toggle-no-toggle-flag




- csvslice
  - [X] `--index` option; Slice a single record (shortcut for --is N --len 1).
  - [X] reconsider option names --is and --ie
    - [x] changed to -S, -E, -L


- csvsed
  - [x] basic test and implementation
  - [x] -m for literal match
  - [x] --max for limiting number of matches per field

- csvsqueeze
  - [X] implement by-column cleaning
  
-- general
  - [x] rename library to `csvkitcat`, `csvkc` for short
  - [x] created alltextutil for common case of reading just text
