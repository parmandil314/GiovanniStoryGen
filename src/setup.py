from cx_Freeze import setup, Executable

# Include your user-made module in the 'packages' list
build_exe_options = {"packages": ["storygen"]}

setup(
    name="giovanni-storygen",
    version="1.0",
    description="Your app description",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py")]
)