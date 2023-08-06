#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from git import Repo, NoSuchPathError, InvalidGitRepositoryError
import logging as log
from .cloneprogress import CloneProgress
from ..model.config import AlloConfig
from ..model.colors import BColors
from ..upgrader import AlloUpgrader
from ..const import *

log.basicConfig(level=log.INFO)


class AlloGit:
    _repo: Repo = None

    token = None
    config: AlloConfig
    upgrader: AlloUpgrader

    def __init__(self, config: AlloConfig, token):
        self.config = config
        self.token = token
        self.init_repo()

    def init_repo(self):
        try:
            self._repo = Repo(self.config.repo_path)
            self._repo.remote().set_url("https://{}:{}@{}/gitlab/{}.git".format(
                    self.config.id_client, self.token, ALLO_URL, self.config.version.git_path))
            self.upgrader = AlloUpgrader(self.config.repo_path)
        except (NoSuchPathError,  InvalidGitRepositoryError):
            os.makedirs(self.config.repo_path, exist_ok=True)
            self._repo = Repo.clone_from(
                "https://{}:{}@{}/gitlab/{}.git".format(
                    self.config.id_client, self.token, ALLO_URL, self.config.version.git_path),
                self.config.repo_path, progress=CloneProgress(), multi_options=['--depth 1'])
            log.info("We have to send event for 'installation'")
            self.upgrader = AlloUpgrader(self.config.repo_path)
            if self.upgrader.do_install() == 0:
                log.info("Version {} installée".format(self._repo.git.describe(tags=True)))
            else:
                print("Erreur d'installation")

        print(BColors.OKGREEN + "✔ {} Version {} detectée".format(self.config.code_produit, self.get_current_version()))

    def get_current_version(self):
        return self._repo.git.describe(tags=True)

    def list_versions(self):
        # Fetch new tags
        self._repo.git.fetch(tags=True)
        return self._repo.tags

    def get_versions_to_pass(self, version: str, reverse: bool = False):
        versions_list = reversed(self.list_versions()) if reverse else self.list_versions()
        versions_to_pass = []
        has_passed_current = False
        for ver in versions_list:
            if has_passed_current:
                versions_to_pass.append(str(ver))
            if str(ver) == self.get_current_version():
                has_passed_current = True
            if version == str(ver):
                break
        return versions_to_pass

    def downgrade_to(self, version: str):
        versions_to_pass = self.get_versions_to_pass(version, True)
        for version in versions_to_pass:
            self.upgrade_to_specific(version)

    def upgrade_to(self, version: str):
        versions_to_pass = self.get_versions_to_pass(version)

        for version in versions_to_pass:
            before_update_version = self.get_current_version()
            if self.upgrade_to_specific(version) != 0:
                log.error("Rollback vers la version {}".format(before_update_version))
                self.upgrade_to_specific(before_update_version)

        log.info("Upgrading to version {} complete with success".format(version))

    def upgrade_to_specific(self, version: str):
        self._repo.git.checkout("tags/{}".format(version))
        return self.upgrader.do_upgrade(version)
