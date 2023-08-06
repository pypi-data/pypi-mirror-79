from setuptools import setup

setup(
    name="tgenv",
    version="1.0.0",
    install_requires=["click", "requests", "tqdm", "PyGithub"],
    description="A tool for managing terragrunt versions",
    url="https://gitlab.com/claudiuskastner/tgenv",
    author="Claudius Kastner",
    keywords="terragrunt terraform versioning",
    author_email="claudiuskastner@kabelmail.de",
    data_files=[('config', ['tgenv/res/default.conf', 'tgenv/res/quotes'])],
    python_requires='>=3.8',
    include_package_data=True,
    packages=["tgenv"],
    entry_points={
        "console_scripts": [
            "tgenv=tgenv.main:cli",
        ]
    }
)
