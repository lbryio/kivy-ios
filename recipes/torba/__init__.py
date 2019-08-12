from toolchain import PythonRecipe, shprint
from os.path import join
import sh, os

class TorbaRecipe(PythonRecipe):
    version = "v0.38.6"
    url = "https://github.com/lbryio/lbry-sdk/archive/{version}.tar.gz"
    
    depends = [
        "python3",
        "setuptools",
        "aiohttp",
        "cffi",
        "coincurve",
        "pbkdf2",
        "cryptography",
        "attrs",
        "pylru"
    ]
    
    def prebuild_arch(self, arch):
        # Use coincurve 7.1.0
        shprint(sh.sed,
                '-i.bak',
                's#coincurve==11.0.0#coincurve==7.1.0#g',
                join(self.get_build_dir(arch.arch), "torba/setup.py"))
        
        # Use cryptography 2.6
        shprint(sh.sed,
                '-i.bak',
                's#cryptography==2.5#cryptography==2.6#g',
                join(self.get_build_dir(arch.arch), "torba/setup.py"))
    
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python3.7', 'site-packages')
        shprint(hostpython, "torba/setup.py", "install", "--prefix", dest_dir, _env=build_env)

recipe = TorbaRecipe()
