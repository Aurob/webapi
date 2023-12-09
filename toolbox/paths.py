import os

domains = ["rau.lol", "rau.dev", "0b.lol", "rau.wiki"]
webpath = "/var/www/"

directory_tree = {}


def contains_index_html(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        if "index.html" in filenames:
            return True
    return False

def get_directory_tree(start_directory):
    tree = {}
    for item in os.listdir(start_directory):
        item_path = os.path.join(start_directory, item)
        if os.path.isdir(item_path) and contains_index_html(item_path):
            dir_tree = get_directory_tree(item_path)
            
            tree[item_path.replace(webpath, '').lower()] = dir_tree

    return tree

def load():
    for domain in domains:
        domain_path = os.path.join(webpath, domain)
        if os.path.exists(domain_path):
            directory_tree[domain] = get_directory_tree(domain_path)

def default():
    return directory_tree

if __name__ != "__main__":
    load()