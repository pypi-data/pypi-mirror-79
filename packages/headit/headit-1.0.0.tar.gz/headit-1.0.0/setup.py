from setuptools import setup
setup(
    name='headit',  # 包名
    python_requires='>=3.4.0', # python环境
    version='1.0.0', # 包的版本
    # description="High aviariable proxy pool client for crawlers.",  # 包简介，显示在PyPI上
    # long_description=read_file('README.md'), # 读取的Readme文档内容
    # long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="518", # 作者相关信息
    author_email='zzycwmx@outlook.com',
    # url='https://github.com/SpiderClub/haipproxy',
    # 指定包信息，还可以用find_packages()函数
    packages=[
        'headit'
    ],
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    include_package_data=True,
    license="MIT",
    keywords=['head', 'header', 'headers'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)