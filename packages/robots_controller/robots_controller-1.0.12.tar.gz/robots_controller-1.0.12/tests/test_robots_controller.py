import pytest


def test_default(tmpdir, get_appmaker, assert_content):

    assert not get_appmaker('django', rollout=False).check_app_name_is_available()
    assert get_appmaker('x7t8', rollout=False).check_app_name_is_available()

    with tmpdir.as_cwd():

        app_maker = get_appmaker()

        settings_str = app_maker.get_settings_string()

        assert 'app_name: dummy' in settings_str
        assert 'Chosen VCS: Git' in settings_str
        assert 'vcs: git'

        assert_content(tmpdir, 'README.rst', [
            'dummy\n=====\n',
            '*testdummydescr*',
            'http://discworld.wrld/librarian/dummy',
        ])

        assert_content(tmpdir, '.gitignore', [
            'docs/_build/',
        ])

        assert_content(tmpdir, 'CHANGELOG', [
            'Unreleased\n-------------\n',
        ])

        assert_content(tmpdir, 'setup.py', [
            "author='The Librarian',",
            "author_email='librarian@discworld.wrld',",
        ])

        assert_content(tmpdir, 'setup.cfg', [
            'universal = 1'
        ])

        assert_content(tmpdir, 'docs/source/conf.py', [
            'from dummy import VERSION_STR'
        ])

def test_tpl_userdefined(tmpdir, get_appmaker, assert_content):

    with tmpdir.as_cwd():

        userdefined = tmpdir.mkdtemp()

        with open(userdefined / 'setup.py', 'w') as f:
            f.write('{% extends parent_template %}\n'
                "{% block install_requires %}{{ super() }}'some',{% endblock %}")

        get_appmaker(templates=['console'])

        assert_content(tmpdir, 'setup.py', [
            "install_requires=[ 'some'",
        ])

def test_tpl_console(tmpdir, get_appmaker, assert_content):

    with tmpdir.as_cwd():

        get_appmaker(templates=['console'])

        assert_content(tmpdir, 'setup.py', [
            "'console_scripts': ['dummy = dummy.cli:main'], ",
        ])


def test_tpl_click(tmpdir, get_appmaker, assert_content):

    with tmpdir.as_cwd():

        get_appmaker(templates=['click'])

        assert_content(tmpdir, 'setup.py', [
            "'click'",
            "'console_scripts': ['dummy = dummy.cli:main'], "
        ])

