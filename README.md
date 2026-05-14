# Houdini-Role

[![AlmaLinux9-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/almalinux9-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/almalinux9-ci-caller.yml) [![Rocky9-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/rocky9-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/rocky9-ci-caller.yml) [![CentOSStream9-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/centosstream9-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/centosstream9-ci-caller.yml) [![Fedora43-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/fedora43-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/fedora43-ci-caller.yml)<br>
[![Ubuntu2404-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/ubuntu2404-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/ubuntu2404-ci-caller.yml) [![Debian13-CI](https://github.com/philnewm/ansible-houdini/actions/workflows/debian13-ci-caller.yml/badge.svg)](https://github.com/philnewm/ansible-houdini/actions/workflows/debian13-ci-caller.yml)

Role description

This role includes a molecule testing setup as a submodule at `molecule/default`

## Structure

```code
📦 ansible-houdini
 ┣ 📂defaults
 ┃ ┗ 📜main.yml
 ┣ 📂files
 ┃ ┣ 📜api_download.py
 ┃ ┣ 📜sesinetd.fc
 ┃ ┣ 📜sesinetd.if
 ┃ ┣ 📜sesinetd.te
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
 ┃ ┣ 📜get_artifacts.yml
 ┃ ┣ 📜install_products.yml
 ┃ ┣ 📜install_sidefxlabs.yml
 ┃ ┣ 📜license_service_selinux.yml
 ┃ ┣ 📜local_license_service.yml
 ┃ ┣ 📜main.yml
 ┃ ┣ 📜present.yml
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
