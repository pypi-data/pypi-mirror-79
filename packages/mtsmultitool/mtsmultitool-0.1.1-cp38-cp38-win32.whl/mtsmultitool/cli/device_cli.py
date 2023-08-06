
import os
import pprint
import argparse
import cbor
import textwrap

from .. import device


def key_gen(args):
    sk, vk = device.gen_key_pair()
    priv, pub = device.export_key_pair(sk, args.name, args.dir)
    print(f'Private key written to "{priv}"')
    print(f'Public key written to "{pub}"')


def key_pub(args):
    sk = device.import_key_pem(args.priv_key_file)
    vk = device.pub_key_from_private(sk)

    output_format = 'wb'
    if args.format == 'hex':
        formatted = vk.hex()
        output_format = 'w'
    elif args.format == 'c':
        formatted = '{ ' + ', '.join([f'0x{b:02x}' for b in vk]) + ' }'
        output_format = 'w'
    else:
        formatted = vk

    if args.output is not None:
        with open(args.output, output_format) as fd:
            fd.write(formatted)
        print(f'Public key written to "{args.output}"')
    else:
        print(formatted)


def patch(args):
    with open(args.original, 'rb') as fd:
        original_image = fd.read()

    with open(args.upgrade, 'rb') as fd:
        upgrade_image = fd.read()

    fw_upgrade = device.create_patch(original_image, upgrade_image, args.bootloader)

    mf = None
    if args.manifest:
        mf = device.generate_manifest(fw_upgrade, args.version, args.class_desc, args.vendor)

        if args.sign is not None:
            sk = device.import_key_pem(args.sign)
            mf = device.sign_manifest(sk, mf)

    output_file = args.output
    if output_file is None:
        output_file = os.path.splitext(args.upgrade)[0]
        output_file += '.patch'
    device.combine(output_file, mf, fw_upgrade.image, args.crc, 0)
    print(f'Firmware patch written to "{output_file}"')


def compress(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()

    fw_upgrade = device.compress(image, args.bootloader)

    mf = None
    if args.manifest:
        mf = device.generate_manifest(fw_upgrade, None, args.class_desc, args.vendor)

        if args.sign is not None:
            sk = device.import_key_pem(args.sign)
            mf = device.sign_manifest(sk, mf)

    output_file = args.output
    if output_file is None:
        output_file = os.path.splitext(args.image)[0]
        output_file += '.lz4'
    device.combine(output_file, mf, fw_upgrade.image, args.crc, 0)
    print(f'Compressed firmware image written to "{output_file}"')


def plain(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()

    fw_upgrade = device.plain(image, args.bootloader)

    mf = None
    if args.manifest:
        mf = device.generate_manifest(fw_upgrade, None, args.class_desc, args.vendor)

        if args.sign is not None:
            sk = device.import_key_pem(args.sign)
            mf = device.sign_manifest(sk, mf)

    output_file = args.output
    if output_file is None:
        output_file = os.path.splitext(args.image)[0]
        output_file += '.upgrade'
    device.combine(output_file, mf, fw_upgrade.image, args.crc, 0)
    print(f'Upgrade written to "{output_file}"')


def manifest(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()

    app_offset = args.bootloader
    if app_offset is None:
        app_offset = 0

    size, digest = device.digest(image, app_offset)
    version = None
    if args.patch is not None:
        image_type = device.FirmwareUpgrade.Type.PATCH
        version = args.patch
    elif args.compressed:
        image_type = device.FirmwareUpgrade.Type.COMPRESSED
    else:
        image_type = device.FirmwareUpgrade.Type.PLAIN
    fw_upgrade = device.FirmwareUpgrade(image[app_offset:], size, digest, image_type)

    mf = device.generate_manifest(fw_upgrade, version, args.class_desc, args.vendor)
    if args.sign is not None:
        sk = device.import_key_pem(args.sign)
        mf = device.sign_manifest(sk, mf)

    if args.apply:
        device.combine(args.image, mf, fw_upgrade.image, False, 0)

    if args.format == 'text':
        pp = pprint.PrettyPrinter(sort_dicts=False)
        output_mf = pp.pformat(mf)
        output_fmt = 'w'
    else:
        output_mf = device.encode_manifest(mf)
        if args.format == 'hex':
            output_mf = output_mf.hex()
            output_fmt = 'w'
        else:
            output_fmt = 'wb'

    if args.output is not None:
        with open(args.output, output_fmt) as fd:
            fd.write(output_mf)
        print(f'Manifest written to "{args.output}"')
    else:
        print(output_mf)


def verify(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()
    try:
        with open(args.pub_key_file, 'rb') as fd:
            pub_key = fd.read()
        sig_res, dig_res = device.verify_manifest(image, pub_key)
        print('Signature: {0}'.format('SUCCESS' if sig_res else 'FAILED'))
        print('Hash digest: {0}'.format('SUCCESS' if sig_res else 'FAILED'))
    except Exception as ex:
        print(ex)


def combine(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()
    with open(args.manifest, 'rb') as fd:
        mf_enc = fd.read()

    output = args.output
    if output is None:
        output = args.image
    mf = cbor.loads(mf_enc)
    device.combine(output, mf, image, args.crc, args.bootloader)
    print(f'Merged file written to "{output}"')


def crc(args):
    with open(args.image, 'rb') as fd:
        image = fd.read()

    appended = False
    output = args.output
    if output is None:
        output = args.image
        appended = True

    with open(output, 'wb') as fd:
        fd.write(image)
        image_crc = device.calculate_crc(image)
        fd.write(image_crc)
        if appended:
            print(f'CRC ({image_crc.hex()}) appended to "{output}"')
        else:
            print(f'Image with CRC ({image_crc.hex()}) written to "{output}"')



def hex_int_arg(arg: str):
    """Validate argument as an integer or convert from hex."""
    try:
        if arg.startswith('0x'):
            return int(arg, 16)
        else:
            return int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError('Must be a decimal or hex starting with "0x"')


def version_arg(arg: str) -> list:
    """Validate argument in a version format x.y.z and convert to list of ints."""
    try:
        v = [int(p) for p in arg.split('.')]
        if len(v) < 3:
            raise ValueError
        return v
    except ValueError:
        raise argparse.ArgumentTypeError('Version must in x.y.z format')


def description(arg: str):
    desc = textwrap.dedent(f'''\
        Commands supporting device firmware upgrade packaging with
        BSDIFF and LZ4 compression with options to apply a SUIT
        manifest and COSE signing using ES256.

        BSDIFF and LZ4 algorithms are modified to use a 512 byte block
        size making patches and compressed images compatible with
        MultiTech\'s bootloader (version 1.0+).

        Provide --help or -h option to see all sub-commands.
    ''')
    print(desc)


def add_parser(subparsers):
    upgrade_parser = subparsers.add_parser('device', help='Device commands')
    upgrade_parser.set_defaults(func=description)
    upgrade_subparsers = upgrade_parser.add_subparsers(metavar='CMD')

    key_gen_parser = upgrade_subparsers.add_parser('keygen', help='Create a key pair for signing a manifest.')
    key_gen_parser.add_argument('name', type=str, help='Name of key')
    key_gen_parser.add_argument('-d', '--dir', type=str, help='Directory path to save key files')
    key_gen_parser.set_defaults(func=key_gen)

    key_pub_parser = upgrade_subparsers.add_parser('keypub', help='Export public key from a private key.')
    key_pub_parser.add_argument('priv_key_file', type=str, help='Path to private key file')
    key_pub_parser.add_argument('-f', '--format', choices=['hex', 'c'], help='Key output format')
    key_pub_parser.add_argument('-o', '--output', type=str,
                                help='Output file path')
    key_pub_parser.set_defaults(func=key_pub)

    patch_parser = upgrade_subparsers.add_parser('patch', aliases=['pa'],
                                         help='Create a firmware patch from old and new images.')
    patch_parser.add_argument('original', type=str, help='Path to original firmware image')
    patch_parser.add_argument('upgrade', type=str, help='Path to upgrade firmware image')
    patch_parser.add_argument('-m', '--manifest', action='store_true',
                              help='Add a manifest to patch image, requires version and class description arguments')
    patch_parser.add_argument('-v', '--version', type=version_arg, help='Version of original firmware in x.y.z format')
    patch_parser.add_argument('-d', '--class_desc', type=str,
                              help='Description of target class used to create class-id in manifest. '
                                   'When using MultiTech\'s bootloader specify the target model (MTDOT or XDOT).')
    patch_parser.add_argument('-n', '--vendor', type=str,
                              help='Vendor DNS used to create vendor-id in manifest. '
                                   'Defaults is for use with MultiTech\'s bootloader. ')
    patch_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                              help='Sign manifest with the specified private key')
    patch_parser.add_argument('-b', '--bootloader', metavar='APPOFFSET', type=hex_int_arg,
                              help='Images contain a bootloader and the application is at APPOFFSET')
    patch_parser.add_argument('-c', '--crc', action='store_true',
                              help='Append CRC32 to end of output file')
    patch_parser.add_argument('-o', '--output', type=str,
                              help='Output file path')
    patch_parser.set_defaults(func=patch)

    compress_parser = upgrade_subparsers.add_parser('compress', aliases=['co'], help='Compress a firmware image.')
    compress_parser.add_argument('image', type=str, help='Path to firmware image')
    compress_parser.add_argument('-m', '--manifest', help='Add a manifest to compressed image', action='store_true')
    compress_parser.add_argument('-d', '--class_desc', type=str,
                                 help='Description of target class used to create class-id in manifest. '
                                      'When using MultiTech\'s bootloader specify the target model (MTDOT or XDOT).')
    compress_parser.add_argument('-n', '--vendor', type=str,
                                 help='Vendor DNS used to create vendor-id in manifest. '
                                      'Defaults is for use with MultiTech\'s bootloader. ')
    compress_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                                 help='Sign manifest with the specified private key')
    compress_parser.add_argument('-b', '--bootloader', metavar='APPOFFSET', type=hex_int_arg,
                                 help='Image contains a bootloader and the application is at APPOFFSET')
    compress_parser.add_argument('-c', '--crc', action='store_true',
                                 help='Append CRC32 to end of output file')
    compress_parser.add_argument('-o', '--output', type=str,
                                 help='Output file path')
    compress_parser.set_defaults(func=compress)

    plain_parser = upgrade_subparsers.add_parser('plain', aliases=['pl'],
                                         help='Create a plain firmware upgrade.')
    plain_parser.add_argument('image', type=str, help='Path to firmware image')
    plain_parser.add_argument('-m', '--manifest', action='store_true', help='Add a manifest to patch image.')
    plain_parser.add_argument('-d', '--class_desc', type=str,
                              help='Description of target class used to create class-id in manifest. '
                                   'When using MultiTech\'s bootloader specify the target model (MTDOT or XDOT).')
    plain_parser.add_argument('-n', '--vendor', type=str,
                              help='Vendor DNS used to create vendor-id in manifest. '
                                   'Defaults is for use with MultiTech\'s bootloader. ')
    plain_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                              help='Sign manifest with the specified private key')
    plain_parser.add_argument('-b', '--bootloader', metavar='APPOFFSET', type=hex_int_arg,
                              help='Images contain a bootloader and the application is at APPOFFSET')
    plain_parser.add_argument('-c', '--crc', action='store_true',
                              help='Append CRC32 to end of output file')
    plain_parser.add_argument('-o', '--output', type=str,
                              help='Output file path')
    plain_parser.set_defaults(func=plain)

    manifest_parser = upgrade_subparsers.add_parser('manifest', aliases=['mf'], help='Create a manifest for a firmware image.')
    manifest_parser.add_argument('image', type=str, help='Path to firmware image')
    manifest_parser.add_argument('-a', '--apply', action='store_true', help='Add manifest to directly to image file')
    manifest_parser.add_argument('-f', '--format', choices=['text', 'hex'], help='Output format')
    manifest_parser.add_argument('-d', '--class_desc', type=str,
                                 help='Description of target class used to create class-id in manifest. '
                                      'When using MultiTech\'s bootloader specify the target model (MTDOT or XDOT).')
    manifest_parser.add_argument('-n', '--vendor', type=str,
                                 help='Vendor DNS used to create vendor-id in manifest. '
                                      'Defaults is for use with MultiTech\'s bootloader. ')
    manifest_parser.add_argument('-p', '--patch', metavar='ORIGVER', type=version_arg,
                                 help='Image is a patch for original version ORIGVER')
    manifest_parser.add_argument('-c', '--compressed', action='store_true',
                                 help='Image is compressed')
    manifest_parser.add_argument('-s', '--sign', metavar='KEYFILE', type=str, default=None,
                                 help='Sign manifest with the specified private key')
    manifest_parser.add_argument('-b', '--bootloader', metavar='APPOFFSET', type=hex_int_arg,
                                 help='Image contains a bootloader and the application is at APPOFFSET')
    manifest_parser.add_argument('-o', '--output', type=str,
                                 help='Output file path')
    manifest_parser.set_defaults(func=manifest)

    combine_parser = upgrade_subparsers.add_parser('combine', aliases=['cb'], help='Combine a manifest with a firmware image.')
    combine_parser.add_argument('manifest', type=str, help='Path to a manifest file')
    combine_parser.add_argument('image', type=str, help='Path to a image file')
    combine_parser.add_argument('-c', '--crc', action='store_true',
                                help='Append CRC32 to end of output file')
    combine_parser.add_argument('-b', '--bootloader', metavar='APPOFFSET', type=hex_int_arg,
                                help='Image contains a bootloader and the application is at APPOFFSET')
    combine_parser.add_argument('-o', '--output', type=str,
                                help='Output file path')
    combine_parser.set_defaults(func=combine)

    verify_parser = upgrade_subparsers.add_parser('verify',
                                          help='Verify signature and hash of a manifest or image with a manifest')
    verify_parser.add_argument('image', type=str, help='Path to a image file')
    verify_parser.add_argument('pub_key_file', type=str, help='Path to public key file')
    verify_parser.set_defaults(func=verify)

    crc_parser = upgrade_subparsers.add_parser('crc', help='Add a CRC32 to an image')
    crc_parser.add_argument('image', type=str, help='Path to a image file')
    crc_parser.add_argument('-o', '--output', type=str,
                            help='Output file path')
    crc_parser.set_defaults(func=crc)
