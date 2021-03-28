import setuptools

setuptools.setup(
    name='domain_rate_limit',
    version='1.0.0',
    author='Dan Kelleher',
    author_email='kelleherjdan@gmail.com',
    maintainer='Dan Kelleher',
    maintainer_email='kelleherjdan@gmail.com',
    description="Rate limit function calls based on URL's domain.",
    packages=['domain_rate_limit'],
    url='https://github.com/djkelleher/domain-rate-limit',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent', 'Topic :: Internet',
    ],
)
