#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'infra-buddy',
        version = '0.1.165',
        description = 'CLI for deploying micro-services',
        long_description = 'CLI for deploying micro-services',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = '',
        author_email = '',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache 2.0',

        url = 'https://github.com/AlienVault-Engineering/infra-buddy',
        project_urls = {},

        scripts = ['scripts/infra-buddy'],
        packages = [
            'infra_buddy',
            'infra_buddy.aws',
            'infra_buddy.commands',
            'infra_buddy.commands.bootstrap',
            'infra_buddy.commands.deploy_cloudformation',
            'infra_buddy.commands.deploy_service',
            'infra_buddy.commands.generate_artifact_manifest',
            'infra_buddy.commands.generate_service_definition',
            'infra_buddy.commands.introspect',
            'infra_buddy.commands.validate_template',
            'infra_buddy.context',
            'infra_buddy.deploy',
            'infra_buddy.notifier',
            'infra_buddy.template',
            'infra_buddy.utility'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'infra_buddy': ['template/builtin-templates.json']
        },
        install_requires = [
            'click',
            'boto3',
            'pydash',
            'jsonschema',
            'requests',
            'datadog'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.6.0',
        obsoletes = [],
    )
