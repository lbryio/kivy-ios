from toolchain import CythonRecipe, shprint
from os.path import join
import os
import sh


class NetifacesRecipe(CythonRecipe):
    name = "netifaces"
    version = "0.10.7"
    url = "https://pypi.python.org/packages/source/n/netifaces/netifaces-{version}.tar.gz"
    library = "libnetifaces.a"
    depends = ["python3", "setuptools"]
    cythonize = False

    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        build_env['CFLAGS'] = '{} -isysroot {}'.format(build_env['CFLAGS'], arch.sysroot)
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python3.7', 'site-packages')
        shprint(hostpython, "setup.py", "install", "--prefix", dest_dir, _env=build_env)


recipe = NetifacesRecipe()
