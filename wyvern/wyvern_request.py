# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union
from urllib.parse import urlparse

import fastapi
from pydantic import BaseModel

from wyvern.components.events.events import LoggedEvent
from wyvern.entities.feature_entities import FeatureDataFrame
from wyvern.entities.identifier import Identifier


@dataclass
class WyvernRequest:
    """
    WyvernRequest is a dataclass that represents a request to the Wyvern service. It is used to pass
    information between the various components of the Wyvern service.

    Attributes:
        method: The HTTP method of the request
        url: The full URL of the request
        url_path: The path of the URL of the request
        json: The JSON body of the request, represented by pydantic model
        headers: The headers of the request
        entity_store: A dictionary that can be used to store entities that are created during the request
        events: A list of functions that return a list of LoggedEvents. These functions are called at the end of
            the request to log events to the event store
        feature_df: The feature data frame that is created during the request
        request_id: The request ID of the request
    """

    method: str
    url: str
    url_path: str
    json: BaseModel
    headers: Dict[Any, Any]

    entity_store: Dict[str, Optional[Dict[str, Any]]]
    # TODO (suchintan): Validate that there is no thread leakage here
    # The list of list here is a minor performance optimization to prevent copying of lists for events
    events: List[Callable[[], List[LoggedEvent[Any]]]]

    feature_df: FeatureDataFrame

    # the key is the name of the model and the value is a map of the identifier to the model score
    model_output_map: Dict[
        str,
        Dict[
            Identifier,
            Union[
                float,
                str,
                List[float],
                Dict[str, Optional[Union[float, str, list[float]]]],
                None,
            ],
        ],
    ]

    request_id: Optional[str] = None
    run_id: str = "0"

    # TODO: params

    @classmethod
    def parse_fastapi_request(
        cls,
        json: BaseModel,
        req: fastapi.Request,
        run_id: str = "0",
        request_id: Optional[str] = None,
    ) -> WyvernRequest:
        """
        Parses a FastAPI request into a WyvernRequest

        Args:
            json: The JSON body of the request, represented by pydantic model
            req: The FastAPI request
            request_id: The request ID of the request

        Returns:
            A WyvernRequest
        """
        return cls(
            method=req.method,
            url=str(req.url),
            url_path=urlparse(str(req.url)).path,
            json=json,
            headers=dict(req.headers),
            entity_store={},
            events=[],
            feature_df=FeatureDataFrame(),
            model_output_map={},
            request_id=request_id,
            run_id=run_id,
        )

    def cache_model_output(
        self,
        model_name: str,
        data: Dict[
            Identifier,
            Union[
                float,
                str,
                List[float],
                Dict[str, Optional[Union[float, str, list[float]]]],
                None,
            ],
        ],
    ) -> None:
        if model_name not in self.model_output_map:
            self.model_output_map[model_name] = {}
        self.model_output_map[model_name].update(data)

    def get_model_output(
        self,
        model_name: str,
        identifier: Identifier,
    ) -> Optional[
        Union[
            float,
            str,
            List[float],
            Dict[str, Optional[Union[float, str, list[float]]]],
            None,
        ]
    ]:
        if model_name not in self.model_output_map:
            return None
        return self.model_output_map[model_name].get(identifier)
