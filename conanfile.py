from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os


class OpenGLConan(ConanFile):
    name = "opengl"
    # version = "virtual"
    description = "Virtual package to provide OpenGL support for other recipes"
    topics = ("conan", "opengl", "gl")
    url = "https://github.com/bincrafters/conan-opengl"
    homepage = "https://opengl.org"
    license = "None"  # TODO: Relax hooks about license attribute for virtual packages? How?

    # TODO: Create virtual package for glu - or add here? Creating it separetly probably prevent options conflict
    # TODO: What about OpenGL ES?
    # TODO: What about OpenCL?
    # TODO: What about EGL?
    # TODO: Add check if system_libs are installed if provider=system?
    # TODO: Try to install system_libs? Probably not
    # TODO: macOS support for < 10.13 (official OpenGL support) and >= 10.13 (no official OpenGL support)
    # TODO: Write a test_package

    settings = {"os"}
    options = {
        "provider": ["system", "conan"],
    }
    default_options = {
        "provider": "system",
    }

    def configure(self):
        if self.settings.os == "Windows" and self.options.provider != "system":
            # While we could just raise an error, this would make the consumption of this package much harder
            # And since the entire idea of this package is to abstract way OpenGL support
            # it is probably better to force the value of the option
            self.output.warning("On Windows only opengl:provider=system is supported! Forcing option")
            self.options.provider = "system"


    def system_requirements(self):
        # This is really, really bad. Is there any better solution to continue support OpenGL on Apple?
        if self.settings.os == "Macos" and tools.os_info.is_macos:
            self.run("brew cask install xquartz")

        if self.options.provider == "system":
            # Note: If you want to disable installation on your system
            # set CONAN_SYSREQUIRES_MODE to disabled
            if self.settings.os == "Linux" and tools.os_info.is_linux:
                if tools.os_info.with_apt or tools.os_info.with_yum:
                    installer = tools.SystemPackageTool()
                    packages = []
                    packages_apt = ["libgl1-mesa-dev"]
                    packages_yum = ["mesa-libGL-devel"]

                    if tools.os_info.with_apt:
                        packages = packages_apt
                    elif tools.os_info.with_yum:
                        packages = packages_yum
                    for package in packages:
                        installer.install(package)

    def requirements(self):
        if self.options.provider == "conan":
            self.requires("mesa/20.0.1@bincrafters/stable")
           
    def package_info(self):
        if self.options.provider == "system":
            if self.settings.os == "Windows":
                self.cpp_info.system_libs.append("opengl32")
            if self.settings.os == "Linux":
                self.cpp_info.system_libs.append("GL")
                # self._add_system_libraries_from_pc("gl")
