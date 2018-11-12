"""Generate markdown files for Hugo contents from Qiita."""
import requests
import re
import configparser

ini = configparser.ConfigParser()
ini.read('./config.ini', 'UTF-8')
QIITA_ACCESS_TOKEN = ini.get('qiita', 'access_token')
QIITA_API_GET_AUTH_USER_ITEMS = '/api/v2/authenticated_user/items?per_page=100'
QIITA_API_ROOT = 'https://qiita.com'
QIITA_API_PARAM_PAGE = str(1)
QIITA_API_PARAM_PER_PAGE = ini.get('qiita', 'per_page')
REQUEST_HEADERS = {'Authorization': 'Bearer ' + QIITA_ACCESS_TOKEN}
HUGO_DEFAULT_EYECATCH = ini.get('hugo', 'default_eyecatch')


def get_qiita_content_list():
    """Get qiita post list."""
    url = QIITA_API_ROOT + QIITA_API_GET_AUTH_USER_ITEMS + '?page=' + QIITA_API_PARAM_PAGE + '&per_page=' + QIITA_API_PARAM_PER_PAGE
    return requests.get(url, headers=REQUEST_HEADERS).json()


def save_as_hugo_md(post):
    """Save markdown file as Hugo content."""
    file_name = get_valid_filename(post['title'])
    full_path = './content/posts/' + file_name + '.md'
    tag_list = [t['name'] for t in post['tags']]
    tags = '["{tag_list_str}"]'.format(tag_list_str='", "'.join(tag_list))
    content_body = post['body']

    img_replace_list = save_inner_image(content_body)
    for img in img_replace_list:
        content_body = content_body.replace(img['qiita_img'], img['hugo_img']).replace(img['qiita_alt'], img['hugo_alt'])

    content = '''
---
title: "{title}"
date: {date}
draft: false
categories: {tags}
tags: {tags}
eyecatch: "{eyecatch}"
---

{content_body}
'''.format(title=post['title'], date=post['created_at'], tags=tags, content_body=content_body, eyecatch=HUGO_DEFAULT_EYECATCH)

    with open(full_path, 'w') as f:
        f.write(content)


def get_valid_filename(fname):
    """
    Get valid file name from post title of Qiita.

    @param string fname
    @return string
    """
    invalid_chars = u'\\/:*?"<>|'
    for invalid_char in invalid_chars:
        fname = fname.replace(invalid_char, u'')

    return fname


def save_inner_image(content_body):
    """
    Save inner image, and return dict list of replacing image links pair.

    @param string content_body
    @return list(dict)
    """
    img_list = re.findall(r'<img width="\d+" alt=".+" src="(.+\..+)">', content_body)
    alt_list = re.findall(r'<img width="\d+" alt="(.+)" src=".+">', content_body)

    replace_list = list()
    for i, qiita_img in enumerate(img_list):
        qiita_alt = alt_list[i]
        save_name = './static/images/{}'.format(qiita_img[qiita_img.rfind('/') + 1:])
        response = requests.get(qiita_img, allow_redirects=False, timeout=10)
        if response.status_code != 200:
            continue

        image = response.content
        with open(save_name, "wb") as fout:
            fout.write(image)

        replace_list.append({
            'qiita_img': qiita_img,
            'qiita_alt': qiita_alt,
            'hugo_img': save_name.replace('./static', ''),
            'hugo_alt': save_name.replace('./static/images/', '')}
        )

    return replace_list

if __name__ == '__main__':
    qitta_posts = get_qiita_content_list()
    for i, p in enumerate(qitta_posts):
        print('{}/{}'.format(i + 1, len(qitta_posts)))
        print("\t", p["title"])
        print("\t", p["url"])
        print("\t", p["created_at"])
        tags = [t["name"] for t in p["tags"]]
        print("\t", ", ".join(tags))
        save_as_hugo_md(p)
