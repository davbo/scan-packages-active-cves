import os
import re
import csv
import click
from collections import defaultdict

PRIORITY_PATTERNS = {
    'low': re.compile('Priority:'),
    'medium': re.compile('Priority: [mh]'),
    'high': re.compile('Priority: [h]'),
}

@click.command()
@click.argument('packages_listing', type=click.File('rb'))
@click.argument('active_cve_directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--ubuntu-version', default='xenial')
@click.option('--priority-threshold', default='medium', type=click.Choice(PRIORITY_PATTERNS.keys()))
def scan_packages(packages_listing, active_cve_directory, ubuntu_version, priority_threshold):
    cves = load_cves(active_cve_directory, ubuntu_version, priority_threshold)
    next(packages_listing) # remove header
    for package_line in packages_listing:
        package, _, _ = package_line.partition(b'/')
        package = package.decode('utf-8')
        if package in cves:
            print(package)
            print(cves[package])


def load_cves(active_cve_directory, ubuntu_version, threshold):
    cves = defaultdict(list)
    package_regex = re.compile('{}_(?P<package_name>[\w_-]*): (?P<status>\w*)'.format(ubuntu_version))
    for filename in filter(lambda fn: fn.startswith('CVE'), os.listdir(active_cve_directory)):
        with open(os.path.join(active_cve_directory, filename)) as f:
            contents = f.read()
            matches = []
            if re.search(PRIORITY_PATTERNS[threshold], contents) != None:
                matches = re.finditer(package_regex, contents)
            for match in matches:
                match_dict = match.groupdict()
                cves[match_dict['package_name']].append((filename, match_dict['status']))
    return cves


if __name__=='__main__':
    scan_packages()
