from toolchain import PythonRecipe, shprint
from os.path import join
import sh, os

class ColoramaRecipe(PythonRecipe):
    version = "0.3.7"
    url = "https://pypi.python.org/packages/source/c/colorama/colorama-{version}.tar.gz"
    depends = ["python3"]
    
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python3.7', 'site-packages')
        shprint(hostpython, "setup.py", "install", "--prefix", dest_dir, _env=build_env)

recipe = ColoramaRecipe()
