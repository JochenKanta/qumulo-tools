# A smattering of Qumulo-oriented API tools

## Write multiple levels of filsystem tree capacity data to a csv

This script will take a start path and walk the tree below that path looking for directories. Each directory will be recorded with it's aggregate capacity below also recorded. Each level must have a name as well.

*Example* Let's say you have directory structure for states and counties:

```
Directory: /all-the-states
    Directory: /all-the-states/WA
        Directory: /all-the-states/WA/King
        Directory: /all-the-states/WA/Pierce
        Directory: /all-the-states/WA/Snohomish
    Directory: /all-the-states/CO
        Directory: /all-the-states/CO/Summit
        Directory: /all-the-states/CO/Arapahoe
```

You would kick off the following command:

`python capacity-tree-data-to-csv.py -s qumulo.storage -u admin -d /all-the-states -l state,county`

* *-s*: Qumulo host to run against
* *-u*: Qumulo api user
* *-d*: Directory to start the walk
* *-l*: Name (or 'tag') for the directory levels. In this example: state = level 1, county = level 2
* *-p*: Optional password on the command line, otherwise you'll be prompted.
* *-o*: Optional path for the file output (default: qumulo-data-by-directory.csv in the working directory)
