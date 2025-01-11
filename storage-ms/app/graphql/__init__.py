"""
The `graphql` module provides resolvers and schemas for GraphQL integration.
It serves as way to avoid under-fetching and over-fetching when filtering items in storage.
"""

from .resolvers import (
    resolve_items)