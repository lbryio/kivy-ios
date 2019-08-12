from toolchain import Recipe, shprint
from os.path import join, exists
import sh
import os
import fnmatch
import shutil


class HostPycparserRecipe(Recipe):
    depends = ["hostpython3"]
    archs = ["x86_64"]
    version = "2.19"
    name = "hostpycparser"
    url = "https://pypi.python.org/packages/source/p/pycparser/pycparser-{version}.tar.gz"

    def install(self):
        import sh
        from toolchain import shprint
        from os import chdir
        arch = self.filtered_archs[0]
        build_dir = self.get_build_dir(arch.arch)
        chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        shprint(hostpython, "setup.py", "install", "--prefix", "{}/hostpython3".format(self.ctx.dist_dir))
    
recipe = HostPycparserRecipe()
