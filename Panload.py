
# -*- coding: utf-8 -*-

import os

import sys

import json

import requests

from subprocess import call

from bs4 import BeautifulSoup


def info () :

    bank = []

    tpn = input ( u'\n\n\tNome para o arquivo : ' )

    tpu = input ( u'\n\tUrl : ' )

    tpe = input ( u'\n\tExtensão do arquivo : ' )

    bank.append ( tpn )

    bank.append ( tpu )

    bank.append ( tpe )

    return bank


def clear () :

    os.system ( 'clear || cls' )


class Archive :

    def __init__ ( self ) :

        pass


    def download ( self, name = None, url = None, ext = None ) :

        if ( name == None or url == None or ext == None ) :

            clear ()

            print ( u'\nError Download - Parameters\n' )

            sys.exit ( 1 )

        self.__name = name

        self.__url = url if url.startswith ( 'https://' ) or url.startswith ( 'http://' ) else 'http://' + url

        self.__ext = ext if ext.startswith ( '.' ) else '.' + ext

        # -

        request = requests.get ( self.__url )

        with open ( self.__name + self.__ext, 'wb' ) as archive :

            for chunk in request.iter_content ( chunk_size = 255 ) :

                if chunk :
                    archive.write ( chunk )

        print ( '\n\n\tDone - {0}\n'.format ( str ( name ) ) )


    def combine ( self, vn, vu, ve, an, au, ae, fn, fe ) :

        print ( '\nLoading ...', end = '\n' )

        self.download ( vn, vu, ve )

        self.download ( an, au, ae )

        self.__comand = 'ffmpeg -i {0}.{1} -i {2}.{3} -c:v copy -c:a aac -map 0:0 -map 1:0 -shortest {4}.{5} && rm -rf {0}.{1} {2}.{3}'.format ( vn, ve, an, ae, fn, fe )

        call ( self.__comand, shell = True )

        clear ()

        print ( '\n\nFile :\n\n\tDone - {0}\n'.format ( fn ) )


    def coub ( self, cn = None, cu = None, ce = None ) :

        self.__cname = cn

        self.__curl = cu if cu.startswith ( 'https://' ) or cu.startswith ( 'http://' ) else 'http://' + cu

        self.__cext = ce

        # -

        self.__coub = requests.get ( self.__curl ).text

        self.__soup = BeautifulSoup ( self.__coub, 'html.parser' )

        self.__soup = str ( self.__soup.find ( id = 'coubPageCoubJson' ) ) [47:-9]

        self.__soup = json.loads ( self.__soup )

        # -

        self.__mp4 = str ( self.__soup['file_versions']['html5']['video']['med']['url'] )

        self.__mp3 = str ( self.__soup['file_versions']['html5']['audio']['high']['url'] )

        self.combine ( 'Vd', self.__mp4, 'mp4', 'Ad', self.__mp3, 'mp3', self.__cname, self.__cext )


Panload = Archive ()


choose = '0'

off = [ '00000000', '0', 'Zero', 'zero' ]

while True :

    clear ();


    print ( '\nMenu :\n\n\t1 - Download\n\n\t2 - Concatenação\n\n\t3 - Download Coub\n' )

    choose = input ( u'Escolha : ' )


    if choose in off :

        clear ()

        sys.exit ( 0 )

    elif choose == '1' :

        clear ();


        print ( '\nDown :')

        bank = info ()

        Panload.download ( * bank )

    elif choose == '2' :

        clear ();


        print ( '\nUnião : ' )

        vn = input ( u'\n\n\tNome para o vídeo : ' )

        vu = input ( u'\n\n\tUrl : ' )

        ve = input ( u'\n\n\tExtensão do vídeo : ' )


        clear ();

        print ( '\nUnião : ' )

        an  = input ( u'\n\n\tNome para o áudio : ' )

        au = input ( u'\n\n\tUrl : ' )

        ae = input ( u'\n\n\tExtensão áudio : ' )


        clear ();

        print ( '\nUnião : ' )

        fn = input ( u'\n\n\tNome para o arquivo convertido : ' )

        fe = input ( u'\n\n\tExtensão para o arquivo convertido : ' )


        clear ()

        Panload.combine ( vn, vu, ve, an, au, ae, fn, fe )

    elif choose == '3' :

        clear ()


        print ( '\nCoub : ' )

        bank_coub = info ()

        Panload.coub ( * bank_coub )

    else :

        print ( '\nOpção invalida' )


    out = input ( u'\nZero para sair, outro digito para continuar : ' )

    if ( out in off ) :

        clear ()

        sys.exit ( 0 )
