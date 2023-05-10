from httpx import Response
from parsel import Selector
from urllib.parse import urljoin

def get_clean_html_tree(
    resp: Response, remove_xpaths=(".//figure", ".//*[contains(@class,'carousel')]")
):
    """cleanup HTML tree from domain specific details like classes"""
    sel = Selector(text=resp.text)
    for remove_xp in remove_xpaths:
        for rm_node in sel.xpath(remove_xp):
            rm_node.remove()
    allowed_attributes = ["src", "href", "width", "height"]
    for el in sel.xpath("//*"):
        for k in list(el.root.attrib):
            if k in allowed_attributes:
                continue
            el.root.attrib.pop(k)
        # turn all link to absolute
        if el.root.attrib.get("href"):
            el.root.attrib["href"] = urljoin(str(resp.url), el.root.attrib["href"])
        if el.root.attrib.get("src"):
            el.root.attrib["src"] = urljoin(str(resp.url), el.root.attrib["src"])
    return sel