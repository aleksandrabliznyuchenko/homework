import re
import urllib.request


def get_plain_text(title):
    try:
        req = urllib.request.Request('https://www.springfieldspringfield.co.uk/movie_script.php?movie=' + title)
        with urllib.request.urlopen(req) as response:
           plain_text = response.read().decode('utf-8')
           return plain_text
    except urllib.error.HTTPError:
        print('Page ' + title + ' does not exist')


def get_screenplay(plain_text):
    regScreenplay = re.compile('                    <div class="scrolling-script-container">.*?                    </div>', re.DOTALL)
    screenplay = regScreenplay.findall(plain_text)
    return screenplay


def screenplay_cleaner(screenplay):
    regTag = re.compile('<.*?>', re.DOTALL)
    regLine = re.compile('\\\\n', re.DOTALL)
    regSlash = re.compile(r'\\', re.DOTALL)
    regList1 = re.compile("\['", re.DOTALL)
    regList2 = re.compile("'\]", re.DOTALL)
    tag_free_screenplay = regTag.sub('', str(screenplay))
    n_free_screenplay = regLine.sub('', tag_free_screenplay)
    screenplay = regSlash.sub('', n_free_screenplay)
    screenplay = regList1.sub('', screenplay)
    clear_screenplay = regList2.sub('', screenplay)
    return clear_screenplay


def file_writer(clear_screenplay, title):
    with open(title + '.txt', 'w', encoding = 'utf-8') as file:
        file.write(clear_screenplay)
        print(title)


def main():
    list_of_titles = ['to-rome-with-love', 'crimes-and-misdemeanors', 'zelig', 'dont-drink-the-water', 
                      'midnight-in-paris', 'vicky-cristina-barcelona', 'the-curse-of-the-jade-scorpion',
                      'annie-hall', 'every-thing-you-always-wanted-to-know-about-sex-but-were-afraid-to-ask',
                      'another-woman', 'deconstructing-harry', 'hollywood-ending', 'small-time-crooks', 'anything-else',
                      'stardust-memories', 'scoop', 'alice', 'radio-days', 'whatever-works', 'broadway-danny-rose',
                      'manhattan', 'match-point', 'husbands-and-wives', 'sleeper', 'sweet-and-lowdown', 'bananas',
                      'cassandras-dream', 'hannah-and-her-sisters', 'shadows-and-fog', 'the-purple-rose-of-cairo',
                      'interiors', 'whats-up-tiger-lily', 'new-york-stories', 'bullets-over-broadway', 'celebrity',
                      'manhattan-murder-mystery', 'take-the-money-and-run', 'love-and-death', 'midsummer-nights-sex-comedy-a',
                      'you-will-meet-a-tall-dark-stranger', 'everyone-says-i-love-you', 'mighty-aphrodite', 'september',
                      'melinda-and-melinda', 'blue-jasmine', 'men-of-crisis-the-harvey-wallinger-story', 'magic-in-the-moonlight',
                      'irrational-man', 'cafe-society', 'wonder-wheel']
    for title in list_of_titles:
        plain_text = get_plain_text(title)
        if plain_text != None:
            screenplay = get_screenplay(plain_text)
            clear_screenplay = screenplay_cleaner(screenplay)
            file_writer(clear_screenplay, title)


if __name__ == "__main__":
    main()
