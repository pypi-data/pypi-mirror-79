from setuptools import setup, Extension

setup(
    name='radarfacerecog',
    version='0.0.5',
    description="Radar Face recogniton, is library to recognize Brazilian politians face's",
    author='Heitor Sampaio',
    author_email='horlando.heitor@gmail.com',
    license='MIT',
    packages=['radarfacerecog'],
    include_package_data=True,
    package_dir={'radarfacerecog': 'radarfacerecog'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['pandas','beautifulsoup4', 'lxml', 'face_recognition', 'numpy', 'opencv-python'],
    python_requires='>=3',
)
