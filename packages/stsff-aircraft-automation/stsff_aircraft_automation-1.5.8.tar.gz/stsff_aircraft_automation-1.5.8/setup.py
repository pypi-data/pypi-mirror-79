import setuptools

setuptools.setup(
    name="stsff_aircraft_automation",
    version="1.5.8",
    author="StepToSky & FlightFactor",
    author_email="technical@flightfactor.aero",
    description="Python scripts for product packages creation, uploading, etc",
    url="https://git.flightfactor.aero/dev-ops/stsff-aircraft-automation",
    #
    package_dir={'': 'shared_script_system',},
    packages=setuptools.find_packages(where='shared_script_system'),
    py_modules=['dds_generator',
                'get_requirements',
                'produce_package',
                'setup_package_info',
                'upload_package',
                'upload_requirements'],
    # binaries
    package_data={'helpers': ['bin/*']},
    #
    install_requires=[
        'requests>=2.18, <3',
        'paramiko>=2.7, <3',
        'scp>=0.13, <1',
        'conan>=1.19, <2',
        'stsff_automation @ git+ssh://git@git.flightfactor.aero/dev-ops/stsff-automation-lib-py.git@1.1.1#egg=stsff_automation',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
)