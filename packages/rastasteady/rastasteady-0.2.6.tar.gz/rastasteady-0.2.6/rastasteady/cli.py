#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import os
import pathlib
from rastasteady.rastasteady import RastaSteady

@click.command(no_args_is_help=True, context_settings=dict(max_content_width=120))

@click.argument('video', type=str, required=True)

@click.option('--no-estabiliza', type=bool, is_flag=True, default=False, help='No estabiliza el video.', show_default=True)
@click.option('--no-rastaview', type=bool, is_flag=True, default=False, help='No crea efecto RastaView del video. Require estabilizar video.', show_default=True)
@click.option('--recortar', type=bool, is_flag=True, default=False, help='Recorta el fichero final para eliminar distorsion. Requiere efecto RastaView.', show_default=True)
@click.option('--dual', type=bool, is_flag=True, default=False, help='Crea fichero dual con video original y procesado. Requiere efecto RastaView.', show_default=True)

@click.version_option('0.2.6')

def cli(video, no_estabiliza, no_rastaview, recortar, dual):
    """RastaSteady es un software de estabilizacion de video para el sistema DJI FPV digital."""
    click.echo('Procesando %s!' % video)

    inputpathlib = pathlib.Path(video)
    currpathlib = pathlib.Path(str(inputpathlib.cwd()) + '/.placeholder')
    tmppathlib = pathlib.Path(str(inputpathlib.cwd()) + '/.rastasteady-' + inputpathlib.name + '/.placeholder')

    myVideo = RastaSteady(video)
    if not no_estabiliza:
        myVideo.stabilize()
        if not no_rastaview:
            myVideo.rastaview()
            if dual:
                myVideo.dual()
            if recortar:
                myVideo.crop()

    for file in ['cropped.mp4', 'dual.mp4', 'rastaview.mp4', 'stabilized.mp4']:
        if tmppathlib.with_name(file).is_file():
            os.rename(tmppathlib.with_name(file), currpathlib.with_name(inputpathlib.stem + '-' + file))
