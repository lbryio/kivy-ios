from toolchain import Recipe, shprint
from os.path import join
import os
import sh


class Sqlite3Recipe(Recipe):
    name = "sqlite3"
    version = '3.24.0'
    # Don't forget to change the URL when changing the version
    url = 'https://www.sqlite.org/2018/sqlite-amalgamation-3240000.zip'
    library = "libsqlite3.a"

    def prebuild_arch(self, arch):
        self.copy_file("Makefile", "Makefile")

    def build_arch(self, arch):
        env = arch.get_env()
        shprint(sh.make, "sqlite3", _env=env)

recipe = Sqlite3Recipe()
