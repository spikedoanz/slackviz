import json

def parse_names(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    names = {}
    for user in data:
        real_name = user.get('real_name') or user.get('profile', {}).get('real_name', '')
        names[user['id']] = real_name
    return names

if __name__ == '__main__':
    names = parse_names('./export/users.json')
    for _ in names:
        print(names[_])