from toolchain import Recipe, shprint
from os.path import join
import os
import sh


class CoincurveRecipe(Recipe):
    name = "coincurve"
    version = "7.1.0"
    url = "https://github.com/ofek/coincurve/archive/{version}.tar.gz"
    depends = ["python3", "setuptools", "libffi", "cffi", "libsecp256k1"]
    cythonize = False

    def prebuild_arch(self, arch):
        if  self.has_marker("patched"):
            return
        
        self.apply_patch("cross_compile.patch")
        self.apply_patch("drop_setup_requires.patch")
        self.apply_patch("find_lib.patch")
        self.apply_patch("no_download.patch")
        
        # remove "tests_require=['pytest>=2.8.7']," string
        shprint(sh.sed,
                '-i.bak',
                's#tests_require=\[\'pytest>=2.8.7\'\],##g',
                join(self.get_build_dir(arch.arch), "setup.py"))
        
        self.set_marker("patched")

    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        
        libsecp256k1 = self.get_recipe('libsecp256k1', self.ctx)
        libsecp256k1_dir = libsecp256k1.get_build_dir(arch.arch)
        
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python3.7', 'site-packages')
        build_env['CFLAGS'] = '{} -I{}'.format(build_env['CFLAGS'], os.path.join(libsecp256k1_dir, 'include'))
        build_env['LDFLAGS'] = '{} -miphoneos-version-min=8.0 -L{}'.format(build_env['LDFLAGS'], os.path.join(libsecp256k1_dir, '.libs'))
        
        print('*******{}'.format(build_env['CFLAGS']))

        shprint(hostpython, "setup.py", "install", "--prefix", dest_dir, _env=build_env)


recipe = CoincurveRecipe()
