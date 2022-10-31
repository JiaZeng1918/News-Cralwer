import hashlib
import multiprocessing
import sys

import pandas as pd
import requests
from newspaper import Article
from newsplease import NewsPlease

session = None


def set_global_session():
    print("URLID")
    global session
    if not session:
        session = requests.Session()


def download_site(url: str):
    try:
        with session.get(url, timeout=(5, 10)) as response:
            article = Article(url)
            article.download()
            article.parse()

            if article.text is not None and response.status_code == 200:
                main_text = NewsPlease.from_html(response.content).maintext
                
                # paragraph here
                article.set_text(main_text.replace('\n', ' '))

                return {'URLID': url, 'MD5': hashlib.md5(url.encode()).hexdigest(), 'Title': article.title,
                        'Text': article.text, 'Top Image': article.top_image, 'Images': article.images, 'Html': response.content}
            else:
                # redirect to error file
                print(url)
                return
    except Exception as e:
        print(url)
        return


def download_sites(urls: list):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        results = pool.map(download_site, urls)
        filter_results = list(filter(None, results))
    return pd.DataFrame(filter_results)


if __name__ == "__main__":
    # Input path example: {path}\url{x}.csv
    # Output path example: {path}\result{x}.csv
    input_path = r"".format(sys.argv[1])
    output_path = r"".format(sys.argv[1])
    input_frame = pd.read_csv(input_path)
    url_list = input_frame['URLID'].to_list()
    info_frame = download_sites(url_list)
    info_frame.to_csv(output_path, index=False)
