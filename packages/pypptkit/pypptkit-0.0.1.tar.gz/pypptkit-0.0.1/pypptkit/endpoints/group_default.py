"""
The default group of operations that pypptkit has
"""

from pytconf import register_endpoint, register_function_group

import pypptkit
import pypptkit.version

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pypptkit commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pypptkit.version.VERSION_STR)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    allow_free_args=True,
)
def extract_text() -> None:
    """
    extract text from ppt files
    """
    pass


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    allow_free_args=True,
)
def extract_links() -> None:
    """
    extract links from ppt files
    """
    pass


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    allow_free_args=True,
)
def download_links() -> None:
    """
    download links from ppt files
    """
    pass


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    allow_free_args=True,
)
def dump_slides() -> None:
    """
    dump object of ppt files
    """
    pass
