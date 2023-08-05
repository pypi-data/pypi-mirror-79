import setuptools

setuptools.setup(
    name='hwhpykit',  # 包名字
    version='1.0.0',  # 包版本
    description='My toolbox',  # 简单描述
    author='louishwh',  # 作者
    author_email='louishwh@gmail.com',  # 作者邮箱
    url='',  # 包的主页
    #packages=['box.cache']
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)

install_requires=[
    'redis>=3.5.3'
]