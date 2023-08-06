import os

from pydantic import HttpUrl, BaseModel
from typing import List, Type

from pypads.app.env import LoggerEnv
from pypads.app.injections.base_logger import TrackedObject
from pypads.app.injections.run_loggers import RunSetup
from pypads.app.misc.managed_git import ManagedGit
from pypads.model.models import TrackedObjectModel, TagMetaModel, ArtifactMetaModel, OutputModel
from pypads.utils.logging_util import WriteFormats


class GitTO(TrackedObject):
    class GitModel(TrackedObjectModel):
        uri: HttpUrl = "https://www.padre-lab.eu/onto/SourceCode-Management"

        source: str = ...
        version: str = ...
        tags: List[TagMetaModel] = []
        git_log: ArtifactMetaModel = ...

        class Config:
            orm_mode = True

    @classmethod
    def get_model_cls(cls) -> Type[BaseModel]:
        return cls.GitModel

    def __init__(self, *args, source, tracked_by, **kwargs):
        super().__init__(*args, source=source, tracked_by=tracked_by, **kwargs)

    def add_tag(self, name, value, description):
        meta = TagMetaModel(name=name, description=description)
        self.tags.append(meta)

        self._store_tag(value, meta)

    def store_git_log(self, name, value, format=WriteFormats.text):
        path = os.path.join(self._base_path(), self._get_artifact_path(name))
        self.git_log = ArtifactMetaModel(path=path, description="Commit logs for the git repository", format=format)

        self._store_artifact(value, self.git_log)

    def _get_artifact_path(self, name):
        return os.path.join(str(id(self)), name)


class IGitRSF(RunSetup):
    """
    Function tracking the source code via git.
    """
    name = "Git Run Setup Logger"
    uri: HttpUrl = "https://www.padre-lab.eu/onto/git-run-logger"
    _dependencies = {"git"}

    class IGitRSFOutput(OutputModel):
        is_a: HttpUrl = "https://www.padre-lab.eu/onto/IGitRSF-Output"
        git_info: GitTO.get_model_cls() = None

    @classmethod
    def output_schema_class(cls) -> Type[OutputModel]:
        return cls.IGitRSFOutput

    def _call(self, *args, _pypads_env: LoggerEnv, _logger_call, _logger_output, **kwargs):
        pads = _pypads_env.pypads
        _pypads_timeout = kwargs.get("_pypads_timeout") if kwargs.get("_pypads_timeout") else 5
        run = pads.api.active_run()
        tags = run.data.tags
        source_name = tags.get("mlflow.source.name", None)
        managed_git: ManagedGit = pads.managed_git_factory(source_name)
        if managed_git:
            repo = managed_git.repo
            git_info = GitTO(tracked_by=_logger_call, source=source_name or repo.working_dir, version=repo.head.commit.hexsha)
            # Disable pager for returns
            repo.git.set_persistent_git_options(no_pager=True)
            try:
                git_info.add_tag("pypads.git.description", repo.description, description="Repository description")
                git_info.add_tag("pypads.git.describe", repo.git.describe("--all"), description="")
                git_info.store_git_log("pypads.git.log", repo.git.log(kill_after_timeout=_pypads_timeout))
                remotes = repo.remotes
                remote_out = "No remotes existing"
                if len(remotes) > 0:
                    remote_out = ""
                    for remote in remotes:
                        remote_out += remote.name + ": " + remote.url + "\n"
                git_info.add_tag("pypads.git.remotes", remote_out, description="Remotes of the repositories")
            except Exception as e:
                _logger_output.set_failure_state(e)
            finally:
                git_info.store(_logger_output,"git_info")
