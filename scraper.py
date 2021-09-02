"""Scans for assignments on viggo using requests and the POST method."""
import re
import configparser
from requests import Session

def get_links(subdomain, info):
    """Gets all assignment links from viggo's assignments page."""
    with Session() as s: # pylint: disable=invalid-name
        login_data = {"UserName": info["user_name"], "Password": info["password"], "fingerprint": info["fingerprint"]}
        s.post(f"https://{subdomain}.viggo.dk/Basic/Account/Login", login_data)
        home_page = s.get("https://nr-aadal.viggo.dk/Basic/HomeworkAndAssignment")
        home_page = str(home_page.content).replace('\\n', '\n').replace('\\r', '\r').replace('\\xc3\\xb8', 'ø').replace('\\xc3\\xa5', 'å').replace('&#xF8;', 'ø').replace('&#xE5;', 'å').replace('\\xc3\\xa6', 'æ').replace('\\xc3\\x98', 'Ø')
    return re.findall(
        "(?<=<a href=\"/Basic/HomeworkAndAssignment/Details/).*?(?=/#modal)",
        home_page,
    )

def extract_data(link, home_page, assignment_data):
    """Extracts data from viggo using regex."""
    assignment_data["url"].append("https://nr-aadal.viggo.dk/Basic/HomeworkAndAssignment/Details/" + link + "/#modal")
    home_page = str(home_page.content).replace('\\n', '\n').replace('\\r', '\r').replace('\\xc3\\xb8', 'ø').replace('\\xc3\\xa5', 'å').replace('&#xF8;', 'ø').replace('&#xE5;', 'å').replace('\\xc3\\xa6', 'æ').replace('\\xc3\\x98', 'Ø').replace('&nbsp;', '')
    new_subject = re.findall("(?<=class=\"ajaxModal\">).*?(?=</a>)", home_page)
    assignment_data["subject"].append(new_subject[0].replace('&#xE6;', 'æ'))
    new_time = re.findall("(?<=<dd>).*?(?= <)", home_page)
    assignment_data["time"].append(new_time[0])
    new_description = re.findall("(?<=<div class=\"content\">).*?(?=</div>)", home_page)
    #assignment_data["description"].append(new_description[0])
    new_author = re.findall("(?<=<p><small class=\"muted\">).*?(?=</small></p>)", home_page)
    assignment_data["author"].append(new_author[0])
    new_file = re.findall("(?<=<a class=\"ajaxModal\" href=\").*?(?=\")", home_page)
    if new_file:
        for j in enumerate(new_file):
            j = j[0]
            new_file[j] = "https://nr-aadal.viggo.dk" + new_file[j]
        file_collection = str(new_file).replace('[', '').replace(']', '').replace('\'', '')
    else:
        file_collection = "None"
    assignment_data["files"].append(file_collection)
    new_file_name = re.findall("(?<=<span>).*?(?=</span>)", home_page)
    if new_file_name:
        for j in enumerate(new_file_name):
            j = j[0]
            new_file_name[j] = new_file_name[j].replace('&#xE6;', 'æ')
        file_name_collection = str(new_file_name).replace('[', '').replace(']', '').replace('\'', '')
    else:
        file_name_collection = "None"
    assignment_data["file_names"].append(file_name_collection)
    return assignment_data, new_description[0]

def get_links_in_post(description):
    """Gets non-labelled hyperlinks in a post and doubles them for future formatting."""
    link_in_post = ''
    if "\" rel=\"noopener noreferrer\" target=\"_blank\">" in description:
        link_in_post = re.findall("(?<=\" rel=\"noopener noreferrer\" target=\"_blank\">).*?(?=</a>)", description)[0]
    return link_in_post, link_in_post + link_in_post

def remove_hex(description, double_link, link_in_post):
    """Filters out hexadecimal symbols from data."""
    pre_hex_removal = description.replace('<p>', '\n').replace('</p>', '').replace('<strong>', '').replace('</strong>', '').replace('<br>', '').replace('<a href=\"', '').replace('\" rel=\"noopener noreferrer\" target=\"_blank\">', '').replace('</a>', '').replace(double_link, link_in_post).replace('&amp;', '&')
    pre_hex_removal = pre_hex_removal.replace('\\x', '|')
    hex_to_remove = re.findall("(?<=\\|).*?(?= |\n)", pre_hex_removal)
    for j in enumerate(hex_to_remove):
        j = j[0]
        replacements = hex_to_remove[j]
        pre_hex_removal = pre_hex_removal.replace(replacements, '')
    description = pre_hex_removal.replace('|', '')
    return description

def format_links(link_in_post, description):
    """Formats links to labelled hyperlinks if possible."""
    finished_description = ''
    if link_in_post != '':
        target = re.findall("(?<=\" rel=\"noopener noreferrer\" target=\"_blank\">).*?(?=</a>)", description)
        href = re.findall("(?<=<a href=\").*?(?=\")", description)
        for j in enumerate(href):
            j = j[0]
            if target[j] != href[j]:
                finished_description = description.replace(target[j], '')
                finished_description = finished_description.replace(href[j], f"[{target[j]}]({href[j]})")
        return finished_description
    return description
def scrape_page(subdomain, link, login_info):
    """Scrapes the contents of a viggo assignment page."""
    with Session() as s: # pylint: disable=invalid-name
        login_data = {"UserName": login_info["user_name"], "Password": login_info["password"], "fingerprint": login_info["fingerprint"]}
        s.post(f"https://{subdomain}.viggo.dk/Basic/Account/Login", login_data)
        home_page = s.get(f"https://{subdomain}.viggo.dk/Basic/HomeworkAndAssignment/Details/{link}/#modal")
    return home_page

def get_assignments(subdomain, info):
    """Function that scans assignments then returns each element in a dictionary."""
    login_info = {
        "user_name": info['USERNAME'],
        "password": info['PASSWORD'],
        "fingerprint": info['FINGERPRINT']
    }
    assignment_data = {
        "subject": [],
        "time": [],
        "description": [],
        "author": [],
        "files": [],
        "file_names": [],
        "url": []
    }
    links = get_links(subdomain, login_info)
    for i in enumerate(links):
        i = i[0]
        home_page = scrape_page(links[i], login_info)
        assignment_data, description = extract_data(links[i], home_page, assignment_data)
        link_in_post, double_link = get_links_in_post(description)
        description = remove_hex(description, double_link, link_in_post)
        description = format_links(link_in_post, description)
        assignment_data['description'].append(description)

    return assignment_data
