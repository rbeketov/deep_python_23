from setuptools import setup, Extension


def main():
    extension_mod = Extension("cjson", sources=["cjson.c"])

    setup(
        name="cjson",
        version="1.0.0",
        description="JSON parser written in C",
        ext_modules=[extension_mod],
    )


if __name__ == "__main__":
    main()
