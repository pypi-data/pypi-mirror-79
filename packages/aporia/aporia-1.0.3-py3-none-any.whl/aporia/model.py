from datetime import datetime
import json
import logging
from typing import Any, cast, Dict, Iterable, List, Optional, Union

import aporia
from aporia.consts import LOGGER_NAME
from aporia.errors import AporiaError, handle_error
from aporia.event_loop import EventLoop
from aporia.graphql_client import GraphQLClient

logger = logging.getLogger(LOGGER_NAME)
FeatureValue = Union[float, int, bool, str]


class BaseModel:
    """Base class for Model objects."""

    def __init__(
        self,
        model_id: str,
        model_version: str,
        environment: Optional[str],
        graphql_client: Optional[GraphQLClient],
        event_loop: Optional[EventLoop],
        debug: bool,
        throw_errors: bool,
    ):
        """Initializes a BaseModel object.

        Args:
            model_id (str): Model identifier
            model_version (str): Model version
            environment (str): Environment's name
            graphql_client (Optional[GraphQLClient]): GraphQL client
            event_loop (Optional[EventLoop]): AsyncIO event loop
            debug (bool): True to enable debug mode
            throw_errors (bool): True to raise exceptions in object creation and set_features
        """
        logger.debug(f"Initializing model object for model {model_id} version {model_version}")
        self.model_id = model_id
        self.model_version = model_version
        self._environment = cast(str, environment)
        self._graphql_client = cast(GraphQLClient, graphql_client)
        self._event_loop = cast(EventLoop, event_loop)
        self._debug = debug
        self._throw_errors = throw_errors
        self._model_ready = False
        self._model_version_exists = False

        # Check model existence
        if event_loop is not None and graphql_client is not None:
            logger.debug(f"Checking if model {model_id} version {model_version} already exists.")
            self._event_loop.run_coroutine(self._check_model_existence())

        if not self._model_ready:
            logger.error("Model object initialization failed - model operations will not work.")

    async def _check_model_existence(self):
        """Checks if the model (and version) exists."""
        query = """
            query CheckModelExists(
                $modelId: String!,
                $modelVersion: String!
            ) {
                modelExists(
                    modelId: $modelId,
                    modelVersion: $modelVersion
                ) {
                    modelExists
                    modelVersionExists
                }
            }
        """
        variables = {
            "modelId": self.model_id,
            "modelVersion": self.model_version,
        }

        try:
            result = (await self._graphql_client.query(query, variables))["modelExists"]
            if not result["modelExists"]:
                raise AporiaError(f"Model {self.model_id} does not exist.")

            self._model_version_exists = result["modelVersionExists"]
            self._model_ready = True

        except Exception as err:
            handle_error(
                message=f"Creating model object failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=self._throw_errors,
                original_exception=err,
            )

    def set_features(
        self, feature_names: List[str], categorical: Optional[Iterable[Union[str, int]]] = None,
    ):
        """Sets feature names and categorical features for the model.

        Args:
            feature_names (List[str]): List of feature names
            categorical (Optional[Iterable[Union[str, int]]], optional): List of categorical
                features - either names or indexes. Defaults to None.
        """
        logger.debug("Setting model features.")
        if not self._model_ready:
            return

        categorical_features = []
        if categorical is not None:
            for feature in categorical:
                if isinstance(feature, str):
                    categorical_features.append(feature_names.index(feature))
                else:
                    categorical_features.append(feature)

        self._event_loop.run_coroutine(self._set_features(feature_names, categorical_features))

    async def _set_features(self, feature_names: List[str], categorical_features: List[int]):
        """Internal, asynchronous implementation for set_features().

        Args:
            feature_names (List[str]): List of feature names
            categorical_features (List[int]): Categorical feature indexes
        """
        query = """
            mutation SetFeatures(
                $modelId: String!,
                $modelVersion: String!,
                $featureNames: [String]!,
                $categoricalFeatures: [Int]!
            ) {
                setFeatures(
                    modelId: $modelId,
                    modelVersion: $modelVersion,
                    featureNames: $featureNames,
                    categoricalFeatures: $categoricalFeatures
                ) {
                    ok
                }
            }
        """

        variables = {
            "modelId": self.model_id,
            "modelVersion": self.model_version,
            "featureNames": feature_names,
            "categoricalFeatures": categorical_features,
        }

        try:
            await self._graphql_client.query(query, variables)
            # If the query didn't fail, then the model version should now exist in the DB
            self._model_version_exists = True
        except Exception as err:
            handle_error(
                message=f"Setting features for {self.model_id} failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=self._throw_errors,
                original_exception=err,
            )

    def add_input_metadata(self, metadata: Dict[str, str]):
        """Adds input metadata fields to the model.

        Args:
            metadata (Dict[str, str]): A dict of field_name: field_type metadata fields. field
                type must be either 'numeric' or 'categorical'.
        """
        self._event_loop.run_coroutine(self._add_metadata(metadata, "INPUT"))

    def add_output_metadata(self, metadata: Dict[str, str]):
        """Adds output metadata fields to the model.

        Args:
            metadata (Dict[str, str]): A dict of field_name: field_type metadata fields. field
                type must be either 'numeric' or 'categorical'.
        """
        self._event_loop.run_coroutine(self._add_metadata(metadata, "OUTPUT"))

    async def _add_metadata(self, metadata: Dict[str, str], designation: str):
        try:
            query = """
                mutation AddMetadata(
                    $modelId: String!,
                    $modelVersion: String!,
                    $metadata: [MetadataFieldInput]!,
                ) {
                    addMetadata(
                        modelId: $modelId,
                        modelVersion: $modelVersion,
                        metadata: $metadata,
                    ) {
                        warnings
                        overwrittenFields {
                            name
                            type
                        }
                    }
                }
            """

            metadata_fields: List[Dict[str, str]] = []
            for value_name, value_type in metadata.items():
                metadata_fields.append(
                    {"name": value_name, "type": value_type.upper(), "designation": designation}
                )

            variables = {
                "modelId": self.model_id,
                "modelVersion": self.model_version,
                "metadata": metadata_fields,
            }

            result = (await self._graphql_client.query(query, variables))["addMetadata"]
            for field in result["overwrittenFields"]:
                logger.warning(
                    f"The type of metadata field {field['name']} was overwritten "
                    f"from {metadata[field['name']]} to {field['type']}."
                )

            for warning in result["warnings"]:
                logger.warning(warning)

        except Exception as err:
            handle_error(
                message=f"Adding {designation} metadata failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=self._throw_errors,
                original_exception=err,
            )

    def log_predict(
        self,
        x: List[FeatureValue],
        y: List[float],
        confidence: Optional[List[float]] = None,
        occurred_at: Optional[datetime] = None,
        **kwargs,
    ):
        """Logs a single prediction.

        Args:
            x (List[FeatureValue]): X values for all of the features in the prediction
            y (List[float]): Prediction result
            confidence (List[float], optional): Prediction confidence. Defaults to None.
            occurred_at (datetime, optional): Prediction timestamp. Defaults to None.
            kwargs (Dict[str, FeatureValue]): Metadata fields, each field must be a single bool,
                int, float or string

        Notes:
            * Many libraries provide a way to convert their objects to lists:
                * numpy array: Use data.tolist()
                * pandas dataframe: Use data.values.tolist()
                * scipy sparse matrix: Use data.toarray().tolist()
            * Metadata fields should be defined with add_input_metadata or add_output_metadata
              before they are passed to log_predict
        """
        self.log_predict_batch(
            x=[x],
            y=[y],
            confidence=None if confidence is None else [confidence],
            occurred_at=occurred_at,
            **{name: [value] for name, value in kwargs.items()},
        )

    def log_predict_batch(
        self,
        x: List[List[FeatureValue]],
        y: List[List[float]],
        confidence: Optional[List[List[float]]] = None,
        occurred_at: Optional[datetime] = None,
        **kwargs,
    ):
        """Logs multiple predictions.

        Args:
            x (List[List[FeatureValue]]): X values for all of the features in each of the predictions
            y (List[List[float]]): Predictions results for each prediction
            confidence (List[List[float]], optional): Confidence for each prediction. Defaults to None.
            occurred_at (datetime, optional): Timestamp for each prediction. Defaults to datetime.now().
            kwargs (Dict[str, List[FeatureValue]]): Metadata fields, each field must be a list of bool,
                int, float or string values, one value for each prediction in the batch

        Notes:
            * Many libraries provide a way to convert their objects to lists:
                * numpy array: Use data.tolist()
                * pandas dataframe: Use data.values.tolist()
                * scipy sparse matrix: Use data.toarray().tolist()
            * Metadata fields should be defined with add_input_metadata or add_output_metadata
              before they are passed to log_predict_batch
        """
        logger.debug(f"Logging {len(y)} predictions")
        if not self._model_ready:
            return

        if not self._model_version_exists:
            logger.warning(
                "Logging prediction failed: features for this model version were not reported."
            )
            return

        metadata = None
        if len(kwargs) > 0:
            metadata = kwargs

        if not self._is_valid_predict_input(x=x, y=y, confidence=confidence, metadata=metadata):
            logger.info("Logging prediction failed: Invalid input.")
            return

        try:
            self._event_loop.run_coroutine(
                coro=self._log_predict_batch(
                    x=x, y=y, confidence=confidence, occurred_at=occurred_at, metadata=metadata
                ),
                await_result=False,
            )
        except Exception as err:
            handle_error(
                message=f"Logging prediction batch failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO,
            )

    async def _log_predict_batch(
        self,
        x: List[List[FeatureValue]],
        y: List[List[float]],
        confidence: Optional[List[List[float]]] = None,
        occurred_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, List[FeatureValue]]] = None,
    ):
        """Internal, asynchronous implementation ofr log_predict_batch.

        Args:
            x (List[List[FeatureValue]]): X values for all of the features in each of the predictions
            y (List[List[float]]): Predictions results for each prediction
            confidence (List[List[float]], optional): Confidence for each prediction. Defaults to None.
            occurred_at (datetime, optional): Timestamp for each prediction. Defaults to datetime.now().
            metadata (Dict[str, List[FeatureValue]], optional): Metadata values. Defaults to None.
        """
        try:
            query = """
                mutation LogPredict(
                    $modelId: String!,
                    $modelVersion: String!,
                    $x: [[FeatureValue]]!,
                    $yPred: [[Float]]!,
                    $confidence: [[Float]],
                    $occurredAt: String,
                    $environment: String!,
                    $metadata: [MetadataValues]
                ) {
                    logPredictions(
                        modelId: $modelId,
                        modelVersion: $modelVersion,
                        x: $x,
                        yPred: $yPred,
                        confidence: $confidence,
                        occurredAt: $occurredAt,
                        environment: $environment,
                        metadata: $metadata
                    ) {
                        warnings
                    }
                }
            """

            metadata_values = None
            if metadata is not None:
                metadata_values = [
                    {"name": name, "values": values} for name, values in metadata.items()
                ]

            variables = {
                "modelId": self.model_id,
                "modelVersion": self.model_version,
                "x": x,
                "yPred": y,
                "confidence": confidence,
                "occurredAt": None if occurred_at is None else occurred_at.isoformat(),
                "environment": self._environment,
                "metadata": metadata_values,
            }

            result = (await self._graphql_client.query(query, variables))["logPredictions"]
            for warning in result["warnings"]:
                logger.warning(warning)

        except Exception as err:
            handle_error(
                message=f"Logging prediction failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO if isinstance(err, AporiaError) else logging.ERROR,
            )

    @staticmethod
    def _is_valid_predict_input(
        x: List[List[FeatureValue]],
        y: List[List[float]],
        confidence: Optional[List[List[float]]] = None,
        metadata: Optional[Dict[str, List[FeatureValue]]] = None,
    ) -> bool:
        if not Model._is_valid_predict_param_list(x):
            logger.debug("Invalid input format for x parameter")
            return False

        if not Model._is_valid_predict_param_list(y):
            logger.debug("Invalid input format for y parameter")
            return False

        if len(x) != len(y):
            logger.debug("Invalid input: x and y should have identical length")
            return False

        if confidence is not None:
            if not Model._is_valid_predict_param_list(confidence):
                logger.debug("Invalid input format for confidence parameter")
                return False

            if len(y) != len(confidence):
                logger.debug("Invalid input: y and confidence should have identical length")
                return False

        if metadata is not None:
            if not Model._is_valid_metadata(metadata=metadata, expected_length=len(x)):
                logger.debug(
                    "Invalid input: each metadata value must be a list with values "
                    "for each prediction in the batch"
                )
                return False

        return True

    @staticmethod
    def _is_valid_metadata(metadata: Dict[str, List[FeatureValue]], expected_length: int) -> bool:
        for metadata_values in metadata.values():
            if not isinstance(metadata_values, list):
                return False

            elif len(metadata_values) != expected_length:
                return False

        return True

    @staticmethod
    def _is_valid_predict_param_list(
        data: Union[List[List[float]], List[List[FeatureValue]]]
    ) -> bool:
        if not isinstance(data, list):
            return False

        if len(data) == 0:
            return False

        if not all((isinstance(data_point, list) and len(data_point) > 0) for data_point in data):
            return False

        return True

    def log_json(self, data: Any):
        """Logs arbitrary data.

        Args:
            data (Any): Data to log, must be JSON serializable
        """
        logger.debug(f"Logging arbitrary data.")
        if not self._model_ready:
            return

        try:
            self._event_loop.run_coroutine(
                coro=self._log_json(data=data), await_result=False,
            )
        except Exception as err:
            handle_error(
                message=f"Logging arbitrary data failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO,
            )

    async def _log_json(self, data: Any):
        """Internal, asynchronous implementation of log_json.

        Args:
            data (Any): Data to log, must be JSON serializable
        """
        try:
            query = """
                mutation LogArbitraryData(
                    $modelId: String!,
                    $modelVersion: String!,
                    $environment: String!,
                    $data: JSONString!
                ) {
                    logArbitraryData(
                        modelId: $modelId,
                        modelVersion: $modelVersion,
                        environment: $environment,
                        data: $data
                    ) {
                        ok
                    }
                }
            """

            variables = {
                "modelId": self.model_id,
                "modelVersion": self.model_version,
                "environment": self._environment,
                "data": json.dumps(data),
            }

            await self._graphql_client.query(query, variables)
        except Exception as err:
            handle_error(
                message=f"Logging arbitrary data failed, error: {str(err)}",
                add_trace=self._debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.INFO if isinstance(err, AporiaError) else logging.ERROR,
            )


class Model(BaseModel):
    """Model object."""

    def __init__(self, model_id: str, model_version: str):
        """Initializes a Model object.

        Args:
            model_id (str): Model identifier.
            model_version (str): Model version
        """
        if aporia.context is None:
            logger.error("Aporia was not initialized.")
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=None,
                environment=None,
                event_loop=None,
                debug=False,
                throw_errors=False,
            )
        else:
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=aporia.context.graphql_client,
                event_loop=aporia.context.event_loop,
                environment=aporia.context.environment,
                debug=aporia.context.debug,
                throw_errors=aporia.context.throw_errors,
            )
