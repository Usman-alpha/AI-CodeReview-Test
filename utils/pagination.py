"""
Pagination utility — clean, well-written code for positive test.
"""

import logging
from dataclasses import dataclass
from typing import Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    """A single page of paginated results."""
    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1


def paginate(items: list[T], page: int = 1, page_size: int = 20) -> Page[T]:
    """
    Return a paginated slice of a list.

    Args:
        items:     Full list of items to paginate
        page:      Page number (1-indexed)
        page_size: Number of items per page (max 100)

    Returns:
        Page object with sliced items and metadata
    """
    page = max(1, page)
    page_size = max(1, min(page_size, 100))

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    sliced = items[start:end]

    logger.debug("Paginated %d items: page %d of %d", total, page, (total + page_size - 1) // page_size)

    return Page(
        items=sliced,
        total=total,
        page=page,
        page_size=page_size,
    )
