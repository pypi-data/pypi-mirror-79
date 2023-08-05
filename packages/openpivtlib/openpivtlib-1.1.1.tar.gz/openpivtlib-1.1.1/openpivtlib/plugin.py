import logging
from typing import Optional, Iterable
from . import util


class Plugin:
    def __init__(self, pipeline: str, job_id: int, args: Optional[dict] = None, data_key: Optional[str] = None):
        self.pipeline = pipeline
        self.job_id = job_id
        self.args = args if args is not None else {}
        self.data_key = data_key

        self.logger = PluginLoggerAdapter(util.get_class_logger(self), self.pipeline, self.job_id)

    def execute(self, data: Optional[dict] = None):
        raise NotImplementedError


class Trigger:
    def __init__(self, pipeline: str):
        self.pipeline = pipeline
        self.logger = TriggerLoggerAdapter(util.get_class_logger(self), self.pipeline)

    def run(self):
        raise NotImplementedError


class PluginLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger: logging.Logger, pipeline: str, job_id: int):
        super().__init__(logger, {})
        self.pipeline = pipeline
        self.job_id = job_id

    def process(self, msg, kwargs):
        return f'[{self.pipeline}:{self.job_id}] {msg}', kwargs


class TriggerLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger: logging.Logger, pipeline: str):
        super().__init__(logger, {})
        self.pipeline = pipeline

    def process(self, msg, kwargs):
        return f'[{self.pipeline}] {msg}', kwargs
