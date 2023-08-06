.. _quickstart:

==========
Quickstart
==========

.. currentmodule:: virt_backup

virt-backup has 4 main functions:
  - :ref:`backup <quickstart_backup>`
  - :ref:`list backups <quickstart_list>`
  - :ref:`restore <quickstart_restore>`
  - :ref:`clean backups <quickstart_clean>`

This page describes how to install virt-backup, create a generic configuration then how to use these 4 functions.

.. contents:: Table of Contents
   :depth: 3


Installation
------------

Run::

  pip3 install virt-backup

Or by using setuptools::

  python3 ./setup.py install

virt-backup is Python 3 compatible only.


Configuration
-------------

.. _quickstart_configuration:


virt-backup is based around the definition of groups. Groups can include or exclude as many domains as needed,
and define the backup properties: compression, disks to backup, where to store the backups, retention, etc..

Groups definition is the biggest part of the configuration.

The configuration is a yaml file. Here is a quite generic one::

  ---

  ########################
  #### Global options ####
  ########################

  ## Be more verbose ##
  debug: False

  ## How many threads (simultaneous backups) to run. Use 0 to use all CPU threads
  ## detected, 1 to disable multitheading for backups, or the number of threads
  ## wanted. Default: 1
  threads: 1


  ############################
  #### Libvirt connection ####
  ############################

  ## Libvirt URI ##
  uri: "qemu:///system"

  ## Libvirt authentication, if needed ##
  username:
  passphrase:


  #######################
  #### Backup groups ####
  #######################

  ## Groups are here to share the same backup options between multiple domains.
  ## That way, it is possible, for example, to have a different policy retention
  ## for a pool of guests in testing than for the one in production.

  ## Define default options for all groups. ##
  ## Here we set the retention parameters for each VM when calling `virt-backup clean`.
  default:
    hourly: 1
    daily: 4
    weekly: 2
    monthly: 5
    yearly: 1

  ## Groups definition ##
  groups:
    ## Group name ##
    test:
      ## Backup directory ##
      target: /mnt/kvm/backups

      ## Use ZSTD compression, configured at lvl 6
      packager: zstd
      packager_opts:
        compression_lvl: 6

      ## When doing `virt-backup backup` without specifying any group, only
      ## groups with the autostart option enabled will be backup.
      autostart: True

      ## Enable the Libvirt Quiesce option when taking the external snapshots.
      ##
      ## From Libvirt documentation: libvirt will try to freeze and unfreeze the guest
      ## virtual machine’s mounted file system(s), using the guest agent. However, if the
      ## guest virtual machine does not have a guest agent, snapshot creation will fail.
      ##
      ## However, virt-backup has a fallback mechanism if the snapshot happens to fail
      ## with Quiesce enabled, and retries without it.
      quiesce: True

      ## Hosts definition ##
      hosts:
        ## Will backup everything.
        - "r:.*"

  # vim: set ts=2 sw=2:


Adapt it and save it either as:

  - ``~/.config/virt-backup/config.yml``
  - ``/etc/virt-backup/config.yml``


Backup
------

.. _quickstart_backup:

All groups set with the `autostart` option to `True` can be started by running::

    $ virt-backup backup

A specific group can be started by running::

    $ virt-backup backup test

When `test` is a group define in the configuration. Multiple groups can be ran with::

    $ virt-backup backup group1 group2 […]

Unicity
~~~~~~~

If multiple groups are backup and some share the same domains to backup, virt-backup will try to see if the backups
could be compatible to avoid doing the exact same backup multiple times.

Example of a groups configuration::

  groups:
    group1:
      target: /mnt/kvm/backups

      packager: zstd
      packager_opts:
        compression_lvl: 6

      ## Hosts definition ##
      hosts:
        - "test1"

    group2:
      target: /mnt/kvm/backups

      packager: zstd
      packager_opts:
        compression_lvl: 6

      ## Hosts definition ##
      hosts:
        - "r:test.*"

    group3:
      target: /mnt/kvm/backups_disk1_only

      packager: tar

      ## Hosts definition ##
      hosts:
        - name: "test1"
          disks:
            - disk1

Here `group1` and `group2` will try to backup the domain `test1` with all its disks, with the same compression
parameters and to the same target directory.  Therefore, `test1` can only be backup once.

However, `group3` specifies that only the disk `disk1` of `test1` has to be backup, and put it in a tarfile in a
different target directory. It is not considered as compatible with what `group1` and `group2` specify, therefore it
will be backup a second time.

Running a backup with this configuration will do 2 backups for `test1`: one shared between `group1` and `group2`, one
for `group3`.
