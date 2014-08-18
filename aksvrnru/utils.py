#-*- codng: utf-8 -*-
import uuid
import urllib
from lxml import html, etree

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

def get_html_desc(url):
    try:
        parser = etree.HTMLParser(encoding='cp1251')
        page = html.parse(url, parser).getroot()
        return etree.tostring(page.xpath('//div[@class="fulltext"]')[0], encoding="utf-8")
    except:
        return ""

def get_id():
    return str(uuid.uuid4())

def retrieve(url, fname):
    urllib.urlretrieve(url, fname)

def get_thumbnail(ipath, size, output, output_format='PNG'):
    image = Image.open(ipath)
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    image.thumbnail(size, Image.ANTIALIAS)
    image.save(output, output_format)

def add_watermark(orig, mark, dest):
    baseim = Image.open(orig)
    logoim = Image.open(mark)
    baseim.paste(logoim, (baseim.size[0]-logoim.size[0], baseim.size[1]-logoim.size[1]), logoim)
    baseim.save(dest,"PNG")
