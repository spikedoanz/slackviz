import os
import subprocess
import json
import re
from datetime import datetime
import pytz

EXPORT_DIRECTORY = './export/'
DIRECTORY = './repo/'
MESSAGE_LEN_CAP = 50 
INCLUDE_USER_NAME = False 

def clean(directory):
    print(f"Deleting non-.py files in: {os.path.abspath(directory)}")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if not item_path.endswith('.py'):
            print(f"Deleting: {item_path}")
            subprocess.run(['rm', '-rf', item_path], check=True)
    print('\n\n---clean---\n\n')

def parse_names(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    names = {}
    for user in data:
        real_name = user.get('real_name') or user.get('profile', {}).get('real_name', '')
        names[user['id']] = real_name
    return names


def init(source_directory):
    # Get the list of items in the source directory
    subprocess.run(['rm', '-rf', DIRECTORY + '.git'], check=True)
    subprocess.run(['git', 'init', DIRECTORY], check=True)
    
    message('TReNDS', '2023', '')
    items = os.listdir(source_directory)
    # Filter out only the directories
    directories = [item for item in items if os.path.isdir(os.path.join(source_directory, item))]
    # Create these directories in the current working directory
    for directory in directories:
        directory = './repo/' + directory 
        os.makedirs(directory, exist_ok=True)

    return directories

def message(user, message, channel, timestamp = 0, name_map = {}):

    def clean_message(message):
        illegal_chars_pattern = r'[@#<>:"\/\\|?*\n\r]+'
        cleaned_message = re.sub(illegal_chars_pattern, '_', message)
        return cleaned_message 
    
    def convert_unix_to_git_date(unix_timestamp):
        date = datetime.fromtimestamp(float(unix_timestamp), tz=pytz.utc)
        return date.strftime("%c %z")

    user = name_map[user] if user in name_map else user
    directory = DIRECTORY + channel + '/' if channel != '' else DIRECTORY 
    message = clean_message(message)

    message = f'{user} - {message}' if INCLUDE_USER_NAME else f'{message}'
    message = '_' if message == '' else message

    message = message.replace(':', '_').replace('/', '_')
    message = message[:MESSAGE_LEN_CAP] if len(message) > 100 else message

    os.makedirs(directory, exist_ok=True)

    # Create a file with the message as the filename
    file_path = os.path.join(directory, message)
    with open(file_path, 'w') as file:
        file.write('')
    try:     
        env = os.environ.copy()
        if timestamp != 0:
            timestamp = convert_unix_to_git_date(timestamp)
            git_date = timestamp
            env['GIT_COMMITTER_DATE'] = git_date
            env['GIT_AUTHOR_DATE'] = git_date

        subprocess.run(['git', '-C', DIRECTORY, 'add',    '.'], check=True, env = env)
        subprocess.run(['git', '-C', DIRECTORY, 'config', 'user.name', user], check=True, env = env)
        subprocess.run(['git', '-C', DIRECTORY, 'config', 'user.email', 'placeholder@example.com'], check=True, env = env)
        subprocess.run(['git', '-C', DIRECTORY, 'commit', '-m', message], check=True, env = env)

    except subprocess.CalledProcessError as e:
        print('SYSTEM LOG: Message skipped')


def parse_slack_logs(file_path):
    channel = os.path.basename(os.path.dirname(file_path))
    with open(file_path, 'r') as file:
        data = json.load(file)

    parsed_data = []
    for message in data:
        log = {
            'user': message.get('user', ''),
            'message': message.get('text', ''),
            'channel': channel,
            'timestamp': message.get('ts', ''),
        }
        parsed_data.append((log['user'],log['message'],log['channel'], log['timestamp']))
    
    return parsed_data

def crawl(directory = EXPORT_DIRECTORY):
    parsed_results = []
    blacklist = ['channels.json', 'integration_logs.json', 'users.json']
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') and file not in blacklist:
                file_path = os.path.join(root, file)
                file_list.append(file_path)


    file_list.sort(key=lambda x: x[-15:])

    for file_path in file_list: 
        parsed_results.extend(parse_slack_logs(file_path))

    return parsed_results




if __name__ == '__main__':
    clean(DIRECTORY)
    init('./export/')

    name_map = parse_names(EXPORT_DIRECTORY+ 'users.json')
    for log in crawl('.'):
        message(*log, name_map)
