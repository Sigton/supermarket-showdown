import cx_Freeze

executables = [cx_Freeze.Executable(script="main.py",
                                    icon="src/resources/icon.ico",
                                    targetName="SupermarketShowdown.exe")]

include_files = ["src"]

packages = ["pygame", "numpy", "random"]

excludes = ["tkinter"]

cx_Freeze.setup(
    name="SupermarketShowdown",
    options={
        "build_exe": {
            "packages": packages,
            "excludes": excludes,
            "include_files": include_files
        }
    },
    executables=executables
)
