from typing import Optional

import nexuscli  # noqa: F401; for mypy and to avoid circular dependency


# When Python 3.6 is deprecated, switch to data class?
class BaseModel:
    """
    Base class for Nexus 3 server objects.

    Args:
        nexus_http: the NexusHttp client instance that will be used to perform operations against
        the Nexus 3 service. You must provide this at instantiation if you plan on calling any
        methods that require connectivity to Nexus.
    """
    def __init__(self, nexus_http: Optional['nexuscli.nexus_http.NexusHttp'] = None, **kwargs):
        self._client: Optional['nexuscli.nexus_http.NexusHttp'] = nexus_http
        self._raw = kwargs  # type: dict
        self._validate_params()

    def _validate_params(self) -> None:
        if self._raw.get('name') is None:
            raise KeyError('name is mandatory in kwargs')

    @property
    def configuration(self) -> dict:
        """
        The model representation as a transformed python dict suitable for converting to JSON and
        passing-through to the Nexus 3 API.
        """
        return self._raw
