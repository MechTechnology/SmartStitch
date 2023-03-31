import argparse

from console.process import ConsoleStitchProcess


def launch():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        dest='input_folder',
        type=str,
        required=True,
        help='Sets the path of Input Folder',
    )
    parser.add_argument(
        "-sh",
        dest='split_height',
        type=positive_int,
        required=True,
        help='Sets the value of the Rough Panel Height',
    )
    parser.add_argument(
        "-t",
        dest='output_type',
        type=str,
        default=".png",
        choices=['.png', '.jpg', '.webp', '.bmp', '.tiff', '.tga', '.psd'],
        help='Sets the type/format of the Output Image Files',
    )
    parser.add_argument(
        "-cw",
        dest='custom_width',
        type=positive_int,
        default=-1,
        help='[Advanced] Forces Fixed Width for All Output Image Files, Default=None (Disabled)',
    )
    parser.add_argument(
        "-dt",
        type=str,
        dest='detection_type',
        default='pixel',
        choices=['none', 'pixel'],
        help='[Advanced] Sets the type of Slice Location Detection, Default=pixel (Pixel Comparison)',
    )
    parser.add_argument(
        "-s",
        dest='detection_senstivity',
        type=int,
        default=90,
        choices=range(0, 101),
        metavar="[0-100]",
        help='[Advanced] Sets the Object Detection Senstivity Percentage, Default=90 (10 percent tolerance)',
    )
    parser.add_argument(
        "-lq",
        dest='lossy_quality',
        type=int,
        default=100,
        choices=range(0, 101),
        metavar="[1-100]",
        help='[Advanced] Sets the quality of lossy file types like .jpg if used, Default=100 (100 percent)',
    )
    parser.add_argument(
        "-ip",
        dest='ignorable_pixels',
        type=positive_int,
        default=5,
        help='[Advanced] Sets the value of Ignorable Border Pixels, Default=5 (5px)',
    )
    parser.add_argument(
        "-sl",
        dest='scan_line_step',
        type=int,
        default=5,
        choices=range(1, 100),
        metavar="[1-100]",
        help='[Advanced] Sets the value of Scan Line Step, Default=5 (5px)',
    )
    kwargs = vars(parser.parse_args())
    process = ConsoleStitchProcess()
    process.run(kwargs)


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue
