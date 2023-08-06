******
device
******


.. code-block::

    multitool device [-h] CMD ...

**Subcommands**

keygen
    Create a key pair for signing a manifest.

keypub
    Export public key from a private key.

patch (pa)
    Create a firmware patch from old and new images.

compress (co)
    Compress a firmware image.

plain (pl)
    Create a plain firmware upgrade.

manifest (mf)
    Create a manifest for a firmware image.

combine (cb)
    Combine a manifest with a firmware image.

verify
    Verify signature and hash of a manifest or image with a manifest.

crc
    Add a CRC32 to an image.

help
    Show help message.

keygen
======

Usage
-----

.. code-block::

    multitool device keygen [-h] [-d DIR] name

positional arguments
^^^^^^^^^^^^^^^^^^^^

name
    Name of key

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

-d DIR, --dir DIR
    Directory path to save key files


keypub
======

Usage
-----

.. code-block::

    multitool device keypub [-h] [-f {hex,c}] [-o OUTPUT] priv_key_file

positional arguments
^^^^^^^^^^^^^^^^^^^^

priv_key_file
    Path to private key file

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

-f {hex,c}, --format {hex,c}
    Key output format

-o OUTPUT, --output OUTPUT
    Output file path



patch
=====

Usage
-----

.. code-block::

    multitool device patch [-h] [-m] [-v VERSION] [-d CLASS_DESC] [-n VENDOR] [-s KEYFILE] [-b APPOFFSET] [-c] [-o OUTPUT] original upgrade

positional arguments
^^^^^^^^^^^^^^^^^^^^

original
    Path to original firmware image

upgrade
    Path to upgrade firmware image

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    Show help message

-m, --manifest
    Add a manifest to patch image, requires version and class description arguments

-v VERSION, --version VERSION
    Version of original firmware in x.y.z format

-d CLASS_DESC, --class_desc CLASS_DESC
    Description of target class used to create class-id in manifest. When using MultiTech's bootloader specify the target model (MTDOT or XDOT).

-n VENDOR, --vendor VENDOR
    Vendor DNS used to create vendor-id in manifest. Defaults is for use with MultiTech's bootloader.

-s KEYFILE, --sign KEYFILE
    Sign manifest with the specified private key

-b APPOFFSET, --bootloader APPOFFSET
    Images contain a bootloader and the application is at APPOFFSET

-c, --crc
    Append CRC32 to end of output file

-o OUTPUT, --output OUTPUT
    Output file path

Examples
--------

Create a patch to upgrade an MDot from 3.3.6 to 3.3.7 from images containing a bootloader and sign the manifest::

    multitool device patch -m -v 3.3.6 -d MTDOT -s mykey.prv -b 0x10000 mdot_image_3.3.6.bin mdot_image_3.3.7.bin

Create a patch to upgrade an XDot from 3.3.6 to 3.3.7 from images containing a bootloader and sign the manifest::

    multitool device patch -m -v 3.3.6 -d XDOT -s mykey.prv -b 0xD000 xdot_image_3.3.6.bin xdot_image_3.3.7.bin


compress
========

Usage
-----

.. code-block::

    multitool device compress [-h] [-m] [-d CLASS_DESC] [-n VENDOR] [-s KEYFILE] [-b APPOFFSET] [-c] [-o OUTPUT] image

positional arguments
^^^^^^^^^^^^^^^^^^^^

image
    Path to firmware image

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

-m, --manifest
    Add a manifest to compressed image
-d CLASS_DESC, --class_desc CLASS_DESC
    Description of target class used to create class-id in manifest. When using MultiTech's bootloader specify the target model (MTDOT or XDOT).

-n VENDOR, --vendor VENDOR
    Vendor DNS used to create vendor-id in manifest. Defaults is for use with MultiTech's bootloader.

-s KEYFILE, --sign KEYFILE
    Sign manifest with the specified private key

-b APPOFFSET, --bootloader APPOFFSET
    Image contains a bootloader and the application is at APPOFFSET

-c, --crc
    Append CRC32 to end of output file

-o OUTPUT, --output OUTPUT
    Output file path


Examples
--------

Create a compressed upgrade for MDot from an image containing a bootloader and sign the manifest::

    multitool device compress -m -d MTDOT -s mykey.prv -b 0x10000 mdot_image_3.3.7.bin

Create a compressed upgrade for XDot from an image containing a bootloader and sign the manifest::

    multitool device compress -m -d XDOT -s mykey.prv -b 0xD000 xdot_image_3.3.7.bin

plain
=====

Usage
-----

.. code-block::

    multitool device plain [-h] [-m] [-d CLASS_DESC] [-n VENDOR] [-s KEYFILE] [-b APPOFFSET] [-c] [-o OUTPUT] image

positional arguments
^^^^^^^^^^^^^^^^^^^^

image
    Path to firmware image

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

-m, --manifest
    Add a manifest to patch image.

-d CLASS_DESC, --class_desc CLASS_DESC
    Description of target class used to create class-id in manifest. When using MultiTech's bootloader specify the target model (MTDOT or XDOT).

-n VENDOR, --vendor VENDOR
    Vendor DNS used to create vendor-id in manifest. Defaults is for use with MultiTech's bootloader.

-s KEYFILE, --sign KEYFILE
    Sign manifest with the specified private key

-b APPOFFSET, --bootloader APPOFFSET
    Images contain a bootloader and the application is at APPOFFSET

-c, --crc
    Append CRC32 to end of output file

-o OUTPUT, --output OUTPUT
    Output file path

Examples
--------

Create a plain upgrade for MDot from an image containing a bootloader and sign the manifest::

    multitool device plain -m -d MTDOT -s mykey.prv -b 0x10000 mdot_image_3.3.7.bin

Create a plain upgrade for XDot from an image containing a bootloader and sign the manifest::

    multitool device plain -d XDOT -s mykey.prv -b 0xD000 xdot_image_3.3.7.bin

manifest
========

Usage
-----

.. code-block::

    multitool device manifest [-h] [-a] [-f {text,hex}] [-d CLASS_DESC] [-n VENDOR] [-p ORIGVER] [-c] [-s KEYFILE] [-b APPOFFSET] [-o OUTPUT] image

positional arguments
^^^^^^^^^^^^^^^^^^^^

image
    Path to firmware image

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

-a, --apply
    Add manifest to directly to image file

-f {text,hex}, --format {text,hex}
    Output format

-d CLASS_DESC, --class_desc CLASS_DESC
    Description of target class used to create class-id in manifest. When using MultiTech's bootloader specify the target model (MTDOT or XDOT).

-n VENDOR, --vendor VENDOR
    Vendor DNS used to create vendor-id in manifest. Defaults is for use with MultiTech's bootloader.

-p ORIGVER, --patch ORIGVER
    Image is a patch for original version ORIGVER

-c, --compressed
    Image is compressed

-s KEYFILE, --sign KEYFILE
    Sign manifest with the specified private key

-b APPOFFSET, --bootloader APPOFFSET
    Image contains a bootloader and the application is at APPOFFSET

-o OUTPUT, --output OUTPUT
    Output file path

Examples
--------

.. code-block::

    multitool device manifest -d XDOT -s mykey.prv -b 0xD000 -o manifest.bin xdot_image_3.3.7.bin
    multitool device combine -b 0xD000 manifest.bin xdot_image_3.3.7.bin

combine
=======

Usage
-----

.. code-block::

    multitool device combine [-h] [-c] [-b APPOFFSET] [-o OUTPUT] manifest image

positional arguments
^^^^^^^^^^^^^^^^^^^^

manifest
    Path to a manifest file

image
    Path to a image file

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

-c, --crc
    Append CRC32 to end of output file

-b APPOFFSET, --bootloader APPOFFSET
    Image contains a bootloader and the application is at APPOFFSET

-o OUTPUT, --output OUTPUT
    Output file path

Examples
--------

verify
======

Usage
-----

.. code-block::

    multitool device verify [-h] image pub_key_file

positional arguments
^^^^^^^^^^^^^^^^^^^^

image
    Path to a image file

pub_key_file
    Path to public key file

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

Examples
--------

crc
===

Usage
-----

.. code-block::

    multitool device crc [-h] [-o OUTPUT] image

positional arguments
^^^^^^^^^^^^^^^^^^^^

image
    Path to a image file

optional arguments
^^^^^^^^^^^^^^^^^^

-h, --help
    show this help message and exit

-o OUTPUT, --output OUTPUT
    Output file path

Examples
--------

