import argparse
from getpass import getpass
from datetime import datetime
from qumulo.rest_client import RestClient


def get_subdirs(rc, path):
    subdirs = []
    res = rc.fs.read_dir_aggregates(path = path, max_entries = 5000)
    for ent in res["files"]:
        if ent['type'] == 'FS_FILE_TYPE_DIRECTORY':
            ent['path'] = path + ('/' if path != '/' else '') + ent['name']
            subdirs.append(ent)
    return sorted(subdirs, key = lambda d : d['name'])

def get_line(ts, typ, ent):
    line = "%(path)s,%(capacity_usage)s,%(num_files)s,%(num_directories)s" % ent
    line = "%s,%s,%s\r\n" % (ts, typ, line)
    return line

def get_capacity_aggregates(rc, start_path, level_names, out_file_name):
    if ',' in level_names[0]:
        level_names = level_names[0].split(",")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    level = 0
    fw = open(out_file_name, "w")
    fw.write("timestamp,directory_level,full_path,capacity_usage,file_count,directory_count\r\n")
    dirs = [start_path]
    while level < len(level_names):
        next_dirs = []
        while dirs:
            current_dir = dirs.pop()
            for ent in get_subdirs(rc, current_dir):
                print("level+name+dir: %s %8s %s" % (level, level_names[level], ent['path']))
                fw.write(get_line(timestamp, level_names[level], ent))
                next_dirs.append(ent['path'])
        level += 1
        dirs = next_dirs
    fw.close()

def main():
    parser = argparse.ArgumentParser(
        description='Walk levels of a known Qumulo filesystem tree and gather capacity metrics'
    )
    parser.add_argument('-s', help='Qumulo hostname', required=True)
    parser.add_argument('-u', help='Qumulo api user', required=True)
    parser.add_argument('-p', help='Qumulo api passord')
    parser.add_argument('-d', help='Starting directory path', required=True)
    parser.add_argument('-o', help='Output file name', default='qumulo-data-by-directory.csv')
    parser.add_argument('-l', nargs='+', help='Level names', required=True)
    args, other_args = parser.parse_known_args()

    if not args.p:
        args.p = getpass()

    creds = {"QHOST": args.s,
             "QUSER": args.u,
             "QPASS": args.p}
    level_names = []

    # initialize the REST client
    rc = RestClient(creds["QHOST"], 8000)
    rc.login(creds["QUSER"], creds["QPASS"])

    get_capacity_aggregates(rc, args.d, args.l, args.o)
    print("Created file: %s" % args.o)

if __name__ == "__main__":
    main()
