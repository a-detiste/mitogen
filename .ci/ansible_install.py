#!/usr/bin/env python

import ci_lib

batches = [
    [
        # Must be installed separately, as PyNACL indirect requirement causes
        # newer version to be installed if done in a single pip run.
        # Separately install ansible based on version passed in from azure-pipelines.yml or .travis.yml
        'pip install "pycparser<2.19" "idna<2.7"',
        'pip install '
            '-r tests/requirements.txt '
            '-r tests/ansible/requirements.txt',
        # 'pip install -q ansible=={0}'.format(ci_lib.ANSIBLE_VERSION)
        # ansible v2.10 isn't out yet so we're installing from github for now
        # encoding is required for installing ansible 2.10 with pip2, otherwise we get a UnicodeDecode error
        'LC_CTYPE=en_US.UTF-8 LANG=en_US.UTF-8 pip install -q {}'.format(ci_lib.ANSIBLE_VERSION)
    ]
]

batches.extend(
    ['docker pull %s' % (ci_lib.image_for_distro(distro),)]
    for distro in ci_lib.DISTROS
)

ci_lib.run_batches(batches)

# after ansible is installed, install common collections until ansible==2.10 comes out
ci_lib.run('ansible-galaxy collection install community.general')
ci_lib.run('ansible-galaxy collection install ansible.netcommon')
ci_lib.run('ansible-galaxy collection install ansible.posix')
