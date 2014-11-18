__author__ = 'jacek'

import csv


class SiteMap(object):
    def __init__(self):
        self.direct_children = []
        self.subsite = {}

    def add_direct_child(self, element):
        self.direct_children.append(element)

    def add_subsite(self, key, value):
        self.subsite[key] = value

    def get_subsite(self, key):
        return self.subsite.get(key)


    def to_str(self):
        website_structure_string = ''

        for current_level_site in self.direct_children:
            website_structure_string += "\t" + str(current_level_site) + "\n"

        if self.subsite:
            for next_level, subsites in self.subsite.items():
                website_structure_string += str(next_level) + "\n"
                website_structure_string += subsites.to_str() + "\n"

        return website_structure_string

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()


def read_file(file_path):
    csv.register_dialect('tab', delimiter='\t', quoting=csv.QUOTE_NONE)

    with open(file_path, 'r') as file_handler:
        aliases, statuses, data = zip(*[line for line in csv.reader(file_handler, dialect='tab')])
    file_handler.close()

    splitted_aliases = list(line[3:] for line in (url.split("/") for url in aliases))

    return splitted_aliases


def organise_websites(splitted_aliases):
    root = SiteMap()

    for tuple in splitted_aliases:
        current_node = root

        for element in tuple:
            if "." in element:
                current_node.add_direct_child(element)
            else:
                subsite = current_node.get_subsite(element)

                if subsite:
                    current_node = subsite
                else:
                    site_map = SiteMap()
                    current_node.add_subsite(element, site_map)
                    current_node = site_map

    print root.to_str()

    return root


organise_websites(read_file("/home/jacek/Projects/test/website.map"))
