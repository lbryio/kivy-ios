from toolchain import Recipe, shprint, current_directory
from os.path import join, exists
from multiprocessing import cpu_count
import os
import sh


class LibSecp256k1Recipe(Recipe):
    name = "libsecp256k1"
    version = "b0452e6"
    url = "https://github.com/bitcoin-core/secp256k1/archive/{version}.zip"
    #library = "libsecp256k1.a"

    def build_arch(self, arch):
        env = arch.get_env()
        env['PATH'] = '/bin:/usr/bin:/usr/local/bin'
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        with current_directory(self.get_build_dir(arch.arch)):
            host = arch.arch
            if host == 'arm64':
                host = 'arm'
            
            if not exists('configure'):
                shprint(sh.Command('./autogen.sh'), _env=env)
            shprint(
                sh.Command('./configure'),
                '--host=' + host,
                '--prefix=' + dest_dir,
                '--enable-shared',
                '--enable-module-recovery',
                '--enable-experimental',
                '--enable-module-ecdh',
                _env=env)
            shprint(sh.make, '-j' + str(cpu_count()), _env=env)
            #libs = ['.libs/libsecp256k1.so']
            #self.install_libs(arch, libs)


recipe = LibSecp256k1Recipe()
