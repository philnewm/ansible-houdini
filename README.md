# Houdini-Role

[![Alma9-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/alma9-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/alma9-ci-caller.yml)  [![Rocky9-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/rocky9-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/rocky9-ci-caller.yml)  [![CentOSStream9-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/centosstream9-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/centosstream9-ci-caller.yml)  [![Debian12-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/debian12-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/debian12-ci-caller.yml)  [![Ubuntu2204-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/ubuntu2204-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/ubuntu2204-ci-caller.yml)

Role description

This role includes a vagrant based molecule testing setup as a submodule at `molecule/default`

## Structure

```code
📦 ansible-houdini
 ┣ 📂defaults
 ┃ ┗ 📜main.yml
 ┣ 📂files
 ┃ ┣ 📜api_download.py
 ┃ ┗ 📜sidefx.py
 ┣ 📂meta
 ┃ ┗ 📜main.yml
 ┣ 📂 molecule
 ┃ ┗ 📂 default
 ┃   ┗ 📜, 📜, 📜, scenario_files
 ┣ 📂tasks
 ┃ ┣ 📜absent.yml
 ┃ ┣ 📜apprentice_license.yml
 ┃ ┣ 📜controller_download.yml
 ┃ ┣ 📜dependencies.yml
 ┃ ┣ 📜license_service_selinux.yml
 ┃ ┣ 📜local_license_service.yml
 ┃ ┣ 📜main.yml
 ┃ ┣ 📜prepare_installer.yml
 ┃ ┣ 📜present.yml
 ┃ ┣ 📜purge_snap.yml
 ┃ ┣ 📜remote_download.yml
 ┃ ┣ 📜run_installer.yml
 ┃ ┗ 📜tests.yml
 ┣ 📂vars
 ┃ ┗ 📜main.yml
 ┣ 📜.gitignore
 ┣ 📜.gitmodules
 ┣ 📜README.md
 ┗ 📜requirements.yml

```

Describe and explain role structure.

## Requirements

Elaborate external dependencies and how to use them.

## Role Variables

* defaults/main.yml
  * first_var
  * sec_var
  * third_var
* vars/main.yml
  * first_var
  * sec_var
  * third_var

## Dependencies

List role ansible-galaxy dependencies - if any.

## Example Playbook

Add an example playbook

```yaml
---

tasks:
  - name: Include ansible-houdini present
    ansible.builtin.include_role:
      name: ansible-houdini
    vars:
      state: present

...
```

## License

Add license - if any.

## Notes

Includes special git configuration for submodule files that are most likely to get local overrides
`.git/info/attributes`

```code
molecule/default/cleanup.yml merge=ours
molecule/default/converge.yml merge=ours
molecule/default/verify.yml merge=ours
```

## Changes to role template

* Add github action that flags empty directories on release creation
