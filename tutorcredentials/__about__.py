__version__ = "17.0.0"
__package_version__ = __version__

# Handle version suffix for nightly, just like tutor core.
__version_suffix__ = ""

if __version_suffix__:
    __version__ += "-" + __version_suffix__

