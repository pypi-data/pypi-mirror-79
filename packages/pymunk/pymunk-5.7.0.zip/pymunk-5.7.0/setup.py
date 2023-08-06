import distutils.ccompiler as cc
import os
import os.path
import platform
import subprocess
import sys
from distutils.command.build_ext import build_ext

from setuptools import Extension, setup

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = object


def get_arch():
    if sys.maxsize > 2**32:
        arch = 64
    else:
        arch = 32
    return arch

def get_library_name():
    libname = 'chipmunk'
    if platform.system() == 'Darwin':
        libname = "lib" + libname + ".dylib"
    elif platform.system() == 'Windows':
        libname += ".dll"
    else: # Linux, FreeBSD and others
        libname = "lib" + libname + ".so"
    return libname


class build_chipmunk(build_ext, object):

    def finalize_options(self):
        if platform.system() == 'Windows':
            print("Running on Windows. GCC will be forced used")
            self.compiler = "unix"
        
        return super(build_chipmunk, self).finalize_options()

    def get_outputs(self):
        x = super(build_chipmunk, self).get_outputs()
        
        #print("get_outputs", x)
        #print("get_outputs xoutputs", self.xoutputs)
        return self.xoutputs

    def is_android(self):
        try:
            machine = subprocess.check_output(
                self.compiler.compiler + ['-dumpmachine'])
            return b'android' in machine
        except:
            print("Could not detect if on Android. Defaulting to false.")
            return False

    def run(self):  
        self.compiler = cc.new_compiler(compiler=self.compiler)
        #print(self.compiler.executables)
        if "AR" in os.environ:
            self.compiler.set_executable("archiver", os.environ["AR"])

        if "CC" in os.environ:
            self.compiler.set_executable("compiler", os.environ["CC"])
            self.compiler.set_executable("compiler_so", os.environ["CC"])
            
        if "LD" in os.environ:
            self.compiler.set_executable("linker_so", os.environ["LD"])

        compiler_preargs = ['-std=gnu99', 
                            '-ffast-math', 
                            '-DCHIPMUNK_FFI', 
                            '-g',
                            #'-Wno-unknown-pragmas', 
                            #'-fPIC', 
                            '-DCP_USE_CGPOINTS=0',
                            # '-DCP_ALLOW_PRIVATE_ACCESS']
                            ]

        if not self.debug:
            compiler_preargs.append('-DNDEBUG')

        is_android = self.is_android()

        if "CFLAGS" in os.environ:
            cflags = os.environ["CFLAGS"].split()
            for cflag in cflags:
                x = cflag.strip()
                if x != "":
                    compiler_preargs.append(x)
        else:
            if is_android:
                compiler_preargs += ['-DANDROID']

            if platform.system() == 'Darwin':
                #No -O3 on OSX. There's a bug in the clang compiler when using O3.
                mac_ver_float = float('.'.join(platform.mac_ver()[0].split('.')[:2]))
                if mac_ver_float > 10.12:
                    compiler_preargs += ['-arch', 'x86_64']
                else:
                    compiler_preargs += ['-arch', 'i386', '-arch', 'x86_64']
            
            elif platform.system() == 'Windows':
                compiler_preargs += ['-shared']
                                                
                if get_arch() == 32:
                    # We set the stack boundary with -mincoming-stack-boundary=2
                    # from 
                    # https://mingwpy.github.io/issues.html#choice-of-msvc-runtime 
                    compiler_preargs += ['-O3', 
                                        '-mincoming-stack-boundary=2',
                                        '-m32']
                if get_arch() == 64:
                    compiler_preargs += ['-O3', '-m64']

            else: # Linux, FreeBSD and others
                compiler_preargs += ['-fPIC', '-O3']
                if get_arch() == 64 and not platform.machine().startswith('arm'):
                    compiler_preargs += ['-m64']
                elif get_arch() == 32 and not platform.machine().startswith('arm'):
                    compiler_preargs += ['-m32']
            
        source_folders = [os.path.join('chipmunk_src','src')]
        sources = []
        for folder in source_folders:
            for fn in os.listdir(folder):
                fn_path = os.path.join(folder, fn)
                if fn[-1] == 'c':
                    # Ignore cpHastySpace since it depends on pthread which 
                    # creates a dependency on libwinpthread-1.dll when built 
                    # with  mingw-w64 gcc.
                    # Will prevent the code from being multithreaded, would be
                    # good if some tests could be made to verify the performance
                    # of this.
                    if platform.system() != 'Windows' or fn != "cpHastySpace.c":
                        sources.append(fn_path)
                    #sources.append(fn_path)
                elif fn[-1] == 'o':
                    os.remove(fn_path)
        
        include_dirs = [os.path.join('chipmunk_src','include')]
        
        objs = self.compiler.compile(sources, 
            include_dirs=include_dirs, extra_preargs=compiler_preargs)
            
        linker_preargs = []
        if "LDFLAGS" in os.environ:
            for l in os.environ["LDFLAGS"].split():
                linker_preargs.append(l)
            #linker_preargs.append("-shared")
        else:
            
            if platform.system() == 'Windows':
                if get_arch() == 32:
                    linker_preargs += ['-m32']
                else:
                    linker_preargs += ['-m64']

            elif platform.system() == 'Darwin':
                self.compiler.set_executable('linker_so', 
                ['cc', '-dynamiclib', '-arch', 'i386', '-arch', 'x86_64'])

            else: #Linux, FreeBSD and others
                if platform.machine() == 'x86_64':
                    linker_preargs += ['-fPIC']
                if is_android:
                    linker_preargs += ['-fPIC', '-lm', '-llog']

        if not self.inplace:
            package_dir = os.path.join(self.build_lib, "pymunk")
        else:
            build_py = self.get_finalized_command('build_py')
            package_dir = os.path.abspath(build_py.get_package_dir(".pymunk"))
        self.xoutputs = [os.path.join(package_dir, get_library_name())]
        #package_dir = self.build_lib
        #print("package_dir", package_dir)
        #outpath = os.path.join(package_dir, get_library_name()) 
        self.compiler.link(
            cc.CCompiler.SHARED_LIBRARY, 
            objs, get_library_name(),
            output_dir = package_dir, extra_preargs=linker_preargs)    
                
                        
# todo: add/remove/think about this list
classifiers = [
    'Development Status :: 5 - Production/Stable'
    , 'Intended Audience :: Developers'
    , 'License :: OSI Approved :: MIT License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Games/Entertainment'
    , 'Topic :: Software Development :: Libraries'   
    , 'Topic :: Software Development :: Libraries :: pygame'
    , 'Programming Language :: Python :: 2'
    , 'Programming Language :: Python :: 2.7'
    , 'Programming Language :: Python :: 3'
]

# from distutils.command import bdist
# bdist.bdist.format_commands += ['msi']
# bdist.bdist.format_command['msi'] = ('bdist_msi', "Microsoft Installer") 

with(open('README.rst')) as f:
    long_description = f.read()

source_folders = [os.path.join('chipmunk_src','src')]
sources = []
for folder in source_folders:
    for fn in os.listdir(folder):
        fn_path = os.path.join(folder, fn)
        if fn_path[-1] == 'c':
            sources.append(fn_path)
        elif fn_path[-1] == 'o':
            os.remove(fn_path)
            
extensions = [("pymunk.chipmunk", {
    'sources': sources,
    'include_dirs': [os.path.join('chipmunk_src','include')]
})]

extensions = [Extension("pymunk.chipmunk", sources)]

class bdist_wheel_universal_extension(bdist_wheel):
    """
    bdist_wheel give overly strict tags for python packages that uses native 
    dynamic linked library called from cffi at runtime.

    References
    https://www.python.org/dev/peps/pep-0491/
    https://www.python.org/dev/peps/pep-0427/
    https://www.python.org/dev/peps/pep-0425/
    https://github.com/getsentry/milksnake
    """
    def get_tag(self):
        rv = bdist_wheel.get_tag(self)
        return ('py2.py3', 'none',) + rv[2:]

setup(
    name = 'pymunk',
    url = 'http://www.pymunk.org',
    author = 'Victor Blomqvist',
    author_email = 'vb@viblo.se',
    version = '5.7.0', # remember to change me for new versions!
    description = 'Pymunk is a easy-to-use pythonic 2d physics library',
    long_description = long_description,
    packages = ['pymunk','pymunkoptions', 'pymunk.tests'],
    include_package_data = True,
    license = 'MIT License',
    classifiers = classifiers,
    cmdclass = {
        'build_ext': build_chipmunk,
        'bdist_wheel': bdist_wheel_universal_extension
    },
    command_options={
        'build_sphinx': {
            'build_dir': ('setup.py', 'docs'),
            'source_dir': ('setup.py', 'docs/src')
        }
    },
    # Skip 1.13.1 becaus of issue reported to cffi here: 
    # https://bitbucket.org/cffi/cffi/issues/432/1131-breaks-pymunk-on-linux-in-a-subtle
    install_requires = ['cffi != 1.13.1'], 
    extras_require = {'dev': ['pyglet','pygame','sphinx', 'aafigure']},    
    test_suite = "pymunk.tests",
    ext_modules = extensions,
)
