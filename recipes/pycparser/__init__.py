from os.path import join
from toolchain import PythonRecipe
from toolchain import shprint
import os
import sh


class PycparserRecipe(PythonRecipe):
    version = "2.19"
    name = "pycparser"
    url = "https://pypi.python.org/packages/source/p/pycparser/pycparser-{version}.tar.gz"
    depends = ["python3"]

    '''
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        # manually create expected directory in build directory
        scripts_dir = join("build", "scripts-3.7")
        if not os.path.exists(scripts_dir):
            os.makedirs(scripts_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        pythonpath = join(dest_dir, 'lib', 'python3.7', 'site-packages')
        build_env['PYTHONPATH'] = pythonpath
        build_env['PYTHONHOME'] = '/usr'
        args = [hostpython, "setup.py", "install", "--prefix", dest_dir]
        shprint(*args, _env=build_env)
        #args = [hostpython, "setup.py", "install"]
        #shprint(*args, _env=build_env)
    '''
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python3.7', 'site-packages')
        shprint(hostpython, "setup.py", "install", "--prefix", dest_dir, _env=build_env)

recipe = PycparserRecipe()
