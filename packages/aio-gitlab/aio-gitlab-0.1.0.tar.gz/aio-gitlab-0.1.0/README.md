aio-gitlab
===============

`aio-gitlab` is Python package which allows for faster fetching of resources from Gitlab API utilizing asyncio.

## Why?

`python-gitlab` package provides access to Gitlab API and allows for working with its resources in Python.

One of the shortcomings of `python-gitlab` package is that when fetching resources, it's doing so by only sending requests sequentially and waiting for response before sending the next request. This starts to become a problem when fetching large amounts of resources, as as it can take significant amount of time just to get even rudimentary information about them.

Another problem that this package is trying to solve is dropped connections after 100 pages of paginated content. This may or may not be a problem when using different versions of `python-gitlab` package.
