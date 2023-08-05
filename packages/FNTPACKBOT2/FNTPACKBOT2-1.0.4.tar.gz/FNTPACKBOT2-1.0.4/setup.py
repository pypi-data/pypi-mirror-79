import setuptools
    
setuptools.setup(
    name="FNTPACKBOT2",
    version="1.0.4",
    author="Bryna",
    description="Lobby bot.",
    url="https://www.youtube.com/channel/UCiDx7oYO4f0qbDEzGdgaq_w?view_as=subscriber&pbjreload=101",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'fortnitepy',
        'BenBotAsync',
        'FortniteAPIAsync',
        'uvloop',
        'sanic',
        'aiohttp'
    ],
)
