__author__ = 'Moises Mendes'
__version__ = '0.1.0'
__all__ = [
    'format_text'
]

import typing as tp


def format_text(text: str, **kwargs: tp.Dict[str, tp.Any]) -> str:
    """Format string replacing placeholders with keyword arguments.
    
    :param text: Text containing named placeholders.
    :type text: ``str``
    :param kwargs: Keyword arguments to replace placeholders.
    :type kwargs: ``dict`` from ``str`` to ``any``
    :return: Formatted text.
    :rtype: ``str``
    """
    return text.format(**kwargs)
