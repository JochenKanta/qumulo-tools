# A smattering of Qumulo-oriented API tools

## Write multiple levels of capacity tree data to a csv - `capacity-tree-data-to-csv.py`

This script will take a start path and walk the tree below that path looking for directories. Each directory will be recorded with it's aggregate capacity below also recorded. Each level must have a name as well.

*Example*: Let's say you have directory structure for states and counties:

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

* -s: The Qumulo host to run against
* -u: The Qumulo api user
* -d: The directory to start the walk from
* -l: The name (or 'tag') for the level of directory. In this example: state = level 1, county = level 2
* -p: Optional password on the command line, otherwise you'll be prompted.
* -o: Optional path for the file output (default: qumulo-data-by-directory.csv in the working directory)
