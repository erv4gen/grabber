from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def text_from_html_test(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.get_text()

    return texts


def extract_title(body):
    soup = BeautifulSoup(body, 'html.parser')
    return soup.title.string


def extract_meta(body):
    soup = BeautifulSoup(body, 'html.parser')
    # title = soup.find("meta",  property="og:title")
    # url = soup.find("meta",  property="og:url")

    return soup.find_all('meta')


def prepare_title(string):
    return ''.join(e for e in string if e.isalnum())