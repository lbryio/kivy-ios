from os.path import join
from kivy_ios.toolchain import CythonRecipe, Recipe, shprint
from kivy_ios.context_managers import cd
import os
import sh


class CryptographyRecipe(CythonRecipe):
    name = "cryptography"
    version = "3.1.1"
    url = "https://pypi.python.org/packages/source/c/cryptography/cryptography-{version}.tar.gz"
    library = "libcryptography.a"
    depends = ["host_setuptools3", "host_cffi", "cffi", "asn1crypto", "idna", "six"]
    python_depends = ["setuptools"]
    cythonize = False
    pre_build_ext = True
    include_per_arch = True
    
    def prebuild_arch(self, arch):
        if self.has_marker("patched"):
            return
        self.apply_patch("osrandom.patch")
        self.set_marker("patched")
        
    def dest_dir(self):
        return join(self.ctx.dist_dir, "root", "python3")

    def get_recipe_env(self, arch):
        env = super(CryptographyRecipe, self).get_recipe_env(arch)
        r = self.get_recipe('openssl', self.ctx)
        openssl_dir = r.get_build_dir(arch.arch)
        target_python = Recipe.get_recipe('python3', self.ctx).get_build_dir(arch.arch)
        env['TOOLCHAIN_PREFIX'] = arch.triple
        env['LDSHARED'] = env['CC'] + ' -pthread -shared -Wl'
        env['LDFLAGS'] += ' -L' + target_python 
        
        env['PYTHON_ROOT'] = join(self.ctx.dist_dir, "root", "python3")
        env['CFLAGS'] += ' -I' + env['PYTHON_ROOT'] + '/include/python3.8' + \
                         ' -I' + join(openssl_dir, 'include') + \
                         ' -I' + join(self.ctx.dist_dir, "include", arch.arch, "libffi")
        env['LDFLAGS'] += ' -L' + env['PYTHON_ROOT'] + '/lib' + \
                          ' -L' + openssl_dir + \
                          ' -lpython3.8' + \
                          ' -lssl' + \
                          ' -lcrypto' + \
                          ' -lffi' + \
                          ' -lcffi ' + \
                          ' -lz'
        return env
    
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python3.8', 'site-packages')
        with cd(build_dir):
            shprint(hostpython, "setup.py", "install", "--prefix", dest_dir, _env=build_env)
        
    def postbuild_arch(self, arch):
        py_arch = arch.arch
        if py_arch == "arm64":
            py_arch = "x86_64"
        build_dir = self.get_build_dir(arch.arch)
        build_env = self.get_recipe_env(arch)
        tmp_folder = 'build/temp.macosx-10.15-{}-3.8/build/temp.macosx-10.15-{}-3.8'.format(py_arch, py_arch)
        for o_file in [
            "_openssl.o",
            "_padding.o",
        ]:
            shprint(sh.Command(build_env['AR']),
                "-q",
                "{}/{}".format(self.build_dir, self.library),
                "{}/{}/{}".format(self.build_dir, tmp_folder, o_file))
    

recipe = CryptographyRecipe()
