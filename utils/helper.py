import re
import os
import utils.config as cfg
from datetime import datetime
os.environ['TZ'] = 'UTC'


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

def kukala_image_path_resolve(im_path):
    path_list = im_path.split('/') 
    out = path_list[-2] + '/' + path_list[-1]
    return out

def get_images_from_server(image_path):
    new_image_path = root_path + '/components/' + image_path.split('/')[-1]
    cmd = f"scp -r production-server:{image_path} {new_image_path}"
    os.system(cmd)
    return new_image_path


def datetime_formatter(date_time: str or datetime, date_format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    if type(date_time) is str:
        if '.' in date_time:
            date_time = date_time.split('.')[0]
            return datetime.strptime(date_time, date_format)
        else:
            return datetime.strptime(date_time, date_format)
    if type(date_time) is datetime:
        return date_time.replace(microsecond=0)


def datetime_to_unix(date_time: str or datetime, date_time_format: str = '%Y-%m-%d %H:%M:%S') -> int:
    """
    Convert string to unix datetime
    date_time: String or Date types date time
    date_time_format : format of date
    Returns: Unix date_time
    """
    date = datetime_formatter(date_time, date_time_format)
    return int(date.timestamp() * 1000)


class GeneralCaptionCleaner:
    @staticmethod
    def get_stop_words(stop_word_path: str = f'/components/stopwords.txt'):
        """
        output: stopwords (List)
        This function read a file of Persian stop words (persian) and return it as a list.
        """
        # read from file
        with open(cfg.root_path + stop_word_path, encoding='utf-8') as f:
            content = f.read()
            # create list
            stop_words = content.split()
        return stop_words

    @staticmethod
    def remove_emoji(string):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r' ', string)

    @staticmethod
    def remove_hashtags(caption: str):
        """
        input: original caption (String)
        output: caption without hashtags (String)
        Extract pure caption and remove hashtags.
        """
        caption = re.sub('#(_*[آ-ی0-9]*_*\s*)', '', caption)
        return caption
