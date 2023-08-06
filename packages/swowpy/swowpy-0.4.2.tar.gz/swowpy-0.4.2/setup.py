from distutils.core import setup

setup(
    name = "swowpy",
    packages = ["swowpy"],
    version = "0.4.2",
    description = "Simple wrapper for OpenWeatherMap",
    author = "Yorozuya3",
    author_email = "yorozuya3@protonmail.com",
    url = "https://gitlab.com/Yorozuya3/swowpy",
    keyword = ["weather","openweathermap","swowpy"],
    install_requires=['requests'],
)
