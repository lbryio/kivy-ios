from toolchain import Recipe, shprint
from os.path import join, exists
import sh
import os
import fnmatch
import shutil


class HostSetuptoolsRecipe(Recipe):
    depends = ["openssl", "hostpython3"]
    name = "setuptools"
    archs = ["x86_64"]
    version = "41.0.1"
    url = "https://pypi.python.org/packages/source/s/setuptools/setuptools-{version}.zip"
    cythonize = False

    '''
    def prebuild_arch(self, arch):
        hostpython = sh.Command(self.ctx.hostpython)
        sh.curl("-O",  "https://bootstrap.pypa.io/ez_setup.py")
        shprint(hostpython, "./ez_setup.py")
        # Extract setuptools egg and remove .pth files. Otherwise subsequent
        # python package installations using setuptools will raise exceptions.
        # Setuptools version 28.3.0
        site_packages_path = join(
            self.ctx.dist_dir, 'hostpython3',
            'lib', 'python3.7', 'site-packages')
        os.chdir(site_packages_path)
        with open('setuptools.pth', 'r') as f:
            setuptools_egg_path = f.read().strip('./').strip('\n')
            unzip = sh.Command('unzip')
            shprint(unzip, '-o', setuptools_egg_path)
        os.remove(setuptools_egg_path)
        os.remove('setuptools.pth')
        os.remove('easy-install.pth')
        shutil.rmtree('EGG-INFO')
    '''    
    def install(self):
        import sh
        from toolchain import shprint
        from os import chdir
        arch = self.filtered_archs[0]
        build_dir = self.get_build_dir(arch.arch)
        chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        shprint(hostpython, "setup.py", "install", "--prefix", "{}/hostpython3".format(self.ctx.dist_dir))
    
recipe = HostSetuptoolsRecipe()
