from toolchain import PythonRecipe, shprint
from os.path import join
import sh, os

class LbryRecipe(PythonRecipe):
    version = "v0.38.6"
    url = "https://github.com/lbryio/lbry-sdk/archive/{version}.tar.gz"
    
    
    
    # all other dependencies defined in torba recipe
    depends = [
        "torba",
        "aiohttp",
        #"aioupnp",
        "appdirs",
        "colorama",
        "distro",
        "base58",
        "cffi",
        "cryptography",
        "protobuf",
        "msgpack",
        "ecdsa",
        "pyyaml",
        "docopt",
        "hachoir",

        # Do we still need these?
        "keyring"
    ]
    
    def prebuild_arch(self, arch):
        setup = "lbry/setup.py"

        # Remove aioupnp requirement?
        shprint(sh.sed,
                '-i.bak',
                's#aioupnp==0.0.13##g',
                join(self.get_build_dir(arch.arch), setup))
        
        # Remove certifi requirement since we'll be including our own cacert.pem
        shprint(sh.sed,
                '-i.bak',
                's#certifi>=2018.11.29##g',
                join(self.get_build_dir(arch.arch), setup))
        
        # Use cryptography 2.6
        shprint(sh.sed,
                '-i.bak',
                's#cryptography==2.5#cryptography==2.6#g',
                join(self.get_build_dir(arch.arch), setup))
    
    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = join(dest_dir, 'lib', 'python3.7', 'site-packages')
        shprint(hostpython, "lbry/setup.py", "install", "--prefix", dest_dir, _env=build_env)

recipe = LbryRecipe()
