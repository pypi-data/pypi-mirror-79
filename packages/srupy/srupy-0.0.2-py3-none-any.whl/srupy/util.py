"""Utility classes and functions."""

import re
from collections import defaultdict


def get_namespace(element):
    """Return the namespace of an XML element.
    :param element: An XML element.
    """
    return re.search('({.*})', element.tag).group(1)


def namespace_mapping(identifier, namespaces):
    """Get the namespace-mapped version of the ``identifier``.

    If the ``identifier`` has a namespace, then this is looked up in the ``namespaces`` dictionary. If the namespace
    is found, then it returns text in the format ``ns_localName``.

    :param identifier: The identifier to map
    :type identifier: ``string``
    :param namespaces: Namespaces to use for mapping
    :type namespaces: ``dict``
    """
    if namespaces and identifier:
        match = re.fullmatch(r'(?:\{([^}]+)\})?(.+)', identifier)
        if match:
            if match.group(1) in namespaces:
                if namespaces[match.group(1)]:
                    return f'{namespaces[match.group(1)]}_{match.group(2)}'
                else:
                    return match.group(2)
    return identifier


# https://stackoverflow.com/a/10076823
def etree_to_dict_without_ns(t):
    tag = re.sub(r'\{.*\}', '', t.tag)
    d = {tag: {} if t.attrib else None}

    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict_without_ns, children):
            for k, v in dc.items():
                dd[re.sub(r'\{.*\}', '', k)].append(v)
            d = {tag: {re.sub(r'\{.*\}', '', k): v[0] if len(v) == 1 else v
                         for k, v in dd.items()}}
    if t.attrib:
            d[tag].update(('@' + k, v)
                            for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[tag]['_text'] = text
        else:
            d[tag] = text

    return d


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['_text'] = text
        else:
            d[t.tag] = text
    return d
