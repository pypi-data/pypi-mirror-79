from typing import List, Dict
from datetime import datetime

from google.cloud.bigquery import ScalarQueryParameter  # type: ignore[import]
import pandas as pd  # type: ignore[import]
import pandas_gbq  # type: ignore[import]

from datatosk import types
from datatosk.sources.databases.sql.sql_source import SQLRead
from datatosk.sources.source import Source, SourceParam, SourceWrite


class GBQRead(SQLRead):
    """Interface element for retrieving data from GBQ dataset.

    Attributes:
        project_id: GoogleBigQuery project_id
    """

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def to_list(self) -> types.ListType:
        raise NotImplementedError

    def to_dict(self) -> types.DictType:
        raise NotImplementedError

    def to_pandas(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> pd.DataFrame:

        query_conf: Dict[str, List[types.JSONType]] = {"queryParameters": []}
        if params:
            query_conf["queryParameters"] = self._cast_params(params=params)

        return pandas_gbq.read_gbq(
            query=query,
            project_id=self.project_id,
            configuration={"query": query_conf},
            **kwargs,
        )

    @staticmethod
    def _cast_params(params: types.ParamsType) -> List[types.JSONType]:

        query_params: List[types.JSONType] = []

        if params is None:
            return query_params

        for param_name, param_value in params.items():
            if isinstance(param_value, int):
                type_ = "INT64"
            elif isinstance(param_value, datetime):
                type_ = "TIMESTAMP"
            elif isinstance(param_value, str):
                try:
                    datetime.fromisoformat(param_value)
                except ValueError:
                    type_ = "STRING"
                else:
                    type_ = "TIMESTAMP"
            else:
                raise ValueError(
                    f"`{param_name}` parameter type {type(param_name)} is not supported."
                )

            query_params.append(
                ScalarQueryParameter(
                    name=param_name, type_=type_, value=param_value
                ).to_api_repr()
            )

        return query_params


class GBQSource(Source):
    """GBQ database interface, it enables retrieving data from it.

    Attributes:
        source_name: source identifier.
            Envioronment variables that should be defined:
            - `GBQ_PROJECT_ID_[SOURCE_NAME]`
        project_id: GoogleBigQuery project_id

    Examples:

    Reading GoogleBigQuery Source
    ====================

    >>> import datatosk
    >>> source = datatosk.gbq(source_name="epic_source")
    >>> source.read("SELECT * FROM epic_table")
        superheros        real_name
    0      Ironman       Tony Stark
    1       Batman      Bruce Wayne
    2     Catwoman      Selina Kyle

    Use of params
    -------------

    >>> source = datatosk.gbq(source_name="epic_source")
    >>> source.read(
    ...     "SELECT superheros, real_name"
    ...     "FROM epic_table"
    ...     "WHERE superheroes = @superhero",
    ...     params={"superhero": "Catwoman"}
    ...)
        superheros        real_name
    0     Catwoman      Selina Kyle
    """

    def __init__(self, source_name: str) -> None:
        super().__init__(source_name)
        self.project_id = self.init_params["GBQ_PROJECT_ID"]

    @property
    def params(self) -> List[SourceParam]:
        return [SourceParam(env_name="GBQ_PROJECT_ID")]

    @property
    def read(self) -> GBQRead:
        """Interface element for retrieving data from GBQ dataset.

        Returns:
            Method-like class which can be used to retrieve data in various types.
        """
        return GBQRead(self.project_id)

    @property
    def write(self) -> SourceWrite:
        """Not implemented yet"""
        raise NotImplementedError
