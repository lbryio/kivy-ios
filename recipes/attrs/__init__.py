from toolchain import PythonRecipe, shprint
from os.path import join
import sh, os

class AttrsRecipe(PythonRecipe):
    version = "18.2.0"
    url = "https://pypi.python.org/packages/source/a/attrs/attrs-{version}.tar.gz"
    depends = ["python", "setuptools"]
    
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python2.7', 'site-packages')
        build_env['PYTHONUSERBASE'] = join(self.ctx.dist_dir, "root", "python3");
        shprint(hostpython, "setup.py", "install", "--user", _env=build_env)

recipe = AttrsRecipe()
