from toolchain import PythonRecipe, shprint
from os.path import join
import sh, os

class ServiceIdentityRecipe(PythonRecipe):
    version = "16.0.0"
    url = "https://pypi.python.org/packages/source/s/service_identity/service_identity-{version}.tar.gz"
    depends = ["python", "setuptools", "attrs", "pyasn1", "pyasn1-modules", "pyopenssl"]
    
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python2.7', 'site-packages')
        shprint(hostpython, "setup.py", "install", "--prefix", dest_dir, _env=build_env)

recipe = ServiceIdentityRecipe()
