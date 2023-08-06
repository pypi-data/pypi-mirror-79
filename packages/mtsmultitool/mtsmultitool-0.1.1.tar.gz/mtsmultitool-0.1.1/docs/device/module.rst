******
device
******

Operation Details
=================

Device Firmware Upgrade Packaging
---------------------------------

This tool can package firmware upgrades in three different ways: patch, compressed, or plain.

**Plain** upgrades are the full, unmodified image.  This type of upgrade can be used for targets that don't support delta
or compression.  A manifest and CRC can be added to the image.

**Patch** upgrades are created using the `BSDiff`_ algorithm with `LZ4`_ compression to create a
binary difference for upgrading a specific version.  Note other implementations of BSDiff are not compatible with this
implementation as it is applied in a block-wise fashion.  This method will, in general, create larger larger patch
images but reduces resource requirements on the target.  When creating a patch with a manifest the target version _must_ be specified.

**Compressed** upgrades are created using `LZ4`_ in a using double buffered block method.

When the differences between firmware versions are great enough a compressed image will be smaller.  For very small
images a plain image will be smaller than a compress image due to overhead from the block-wise compression.

Bootloader
^^^^^^^^^^
Any bootloader included in a firmware image must be stripped.  An option to specify the application offset is provided
and will operate on the image start at that address.

CRC
^^^
MultiTech's bootloaders are capable of upgrades over YModem and require a CRC32 to be appended to the image file.  An
option is included to apply the CRC to upgrade images.  Note it is safe to send images with a CRC via FOTA as the
CRC will be ignored by the bootloader.

Manifest
^^^^^^^^
The manifest added to an upgrade image is used to verify the image (image-digest) and tell a bootloader how to apply the
upgrade (compression, delta, etc.).

SUIT
^^^^
Manifests are created following the Software Updates for Internet of Things (`SUIT`_) format which is encoded
as Concise Binary Object Representation (`CBOR`_).

Vendor and Class Identifiers
""""""""""""""""""""""""""""
Vendor and class identifiers should be used by a target device to verify the upgrade image is compatible.  For example,
the class identifier for an MTDOT and an XDOT will be different.  If XDOT firmware is mistakenly sent to an MDOT the
MDOT should not attempt to apply the upgrade.

This tools has options to specify a class description and vendor.  The manifest must have identifiers matching the
target bootloader.  If no vendor is specified `multitech.com` is used.

.. code-block:: python
    :caption: Vendor and class ID creation

    class_desc = 'MTDOT'            # Minimal mDot description
    vendor_dns = 'multitech.com'    # Default if not specified
    vendor_id = uuid.uuid5(uuid.NAMESPACE_DNS, vendor_dns)
    class_id = uuid.uuid3(vendor_id, class_desc)


Patches and Version
"""""""""""""""""""
When creating a patch (delta) upgrade, the version of firmware the upgrade is intended for must be specified.  For
example, when creating a patch to upgrade v3.3.6 to v3.3.7 the original version '3.3.6' must be specified.  This version
can be used by the target to verify compatibility of the patch.

Image Digest and Size
"""""""""""""""""""""
A SHA256 digest of the upgrade is included in the manifest.  When a compressed or patch image are created the digest
is of the applied upgrade.  When the target applies a patch, the digest of the final patched image should match the
image digest in the manifest.  The same applies for the included image size.

COSE
^^^^
Manifests can optionally be signed using Elliptic Curve Digital Signature Algorithm (`ECDSA`_).  A CBOR
Object Signing and Encryption (`COSE`_) authentication wrapper is added to the manifest containing the SHA256
digest of the SUIT manifest encoded as CBOR and a signature.

Verification
""""""""""""
Authenticity of the manifest can be verified by the target by computing the SHA256 digest of the SUIT portion and
comparing it to the payload digest included in the COSE wrapper then use a pre-shared public key to validate the
signature.

1. Compute SHA256 digest of the SUIT portion of the manifest
2. Compare the computed digest against the payload digest included in the COSE wrapper
3. Use a pre-shared public key to verify the signature

Contents
^^^^^^^^

.. code-block:: python
    :caption: Manifest content as Python dictionary

    {
        2: [                                    # authentication-wrapper
            { 1: -7 },                          #  protected alg: ES256
            { },                                #  unprotected
            [                                   #  payload
                2,                              #   algorithm-id (sha256)
                <suit digest>                   #   payload-digest
            ],
            <suit signature>                    #  signature
        ],
        3: {                                    # manifest
            1: 1,                               #  manifest-version
            2: 1,                               #  manifest-sequence-number
            3: {                                #  common
                2: [[b'\0']],                   #   components
                4: [                            #   common-sequence
                    20,                         #    directive-override-parameters
                    {
                        1: <vendor_id>,         #     vendor-id
                        2: <class_id>,          #     class-id
                        3: [                    #     image-digest
                            2,                  #      algorithm-id (sha256)
                            <upgrade digest>    #      digest-bytes
                        ]
                        14: <upgrade size>      #     image-size
                        28: [ <version> ]       #     version (optional)
                    },
                    1, 0xf6,                    #    condition-vendor-identifier
                    2, 0xf6,                    #    condition-class-identifier
                    28, 0xf6                    #    condition-version (optional)
                ]
            },
            9: [                                #  install
                19,
                {                               #   directive-set-parameters
                    21: "file:///fw_upgrade.bin",
                    20: 1,                      #    unpack-info: delta (optional)
                    19: 4                       #    compression-info: lz4 (optional)
                },
                23, 0xf6                        #  directive-copy
            ],
            10: [                               #  validate
                3, 0xf6                         #   condition-image-match
            ],
            12: [                               #  run
                23, 0xf6                        #   directive-run
            ]
        }
    }


.. _SUIT: https://tools.ietf.org/html/draft-ietf-suit-manifest-04
.. _COSE: https://tools.ietf.org/html/rfc8152
.. _CBOR: https://tools.ietf.org/html/rfc7049
.. _ECDSA: https://tools.ietf.org/html/rfc6979
.. _BSDIFF: http://www.daemonology.net/bsdiff
.. _LZ4: https://github.com/lz4/lz4
.. _ARM_MBED_EDGE: https://github.com/ARMmbed/mbed-edge

Usage
=====

.. automodule:: mtsmultitool.device
    :members:
