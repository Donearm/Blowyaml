#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2013, Gianluca Fiore
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
###############################################################################
#
# Modified from http://code.activestate.com/recipes/496763-a-simple-pycrypto-blowfish-encryption-script/
# to whom go all the credits for the Blowfish implementation (the BFCipher class)

__author__ = "Gianluca Fiore"
__copyright__ = ""
__credits__ = ""
__license__ = "GPL"
__version__ = "0.1"
__mantainer__ = ""
__date__ = "20130329"
__email__ = "forod.g@gmail.com"
__status__ = "beta"

import os
import sys
import argparse
from random import randrange
from Crypto.Cipher import Blowfish
from getpass import getpass

class BFCipher:
    def __init__(self, pword):
        self.__cipher = Blowfish.new(pword)

    def encrypt(self, file_buffer):
        ciphertext = self.__cipher.encrypt(self.__pad_file(file_buffer))
        return ciphertext

    def decrypt(self, file_buffer):
        try:
            cleartext = self.__depad_file(self.__cipher.decrypt(file_buffer))
            return cleartext
        except ValueError:
            # probably a not previously encrypted file, exit
            print("Input file doesn't seem encrypted, check your parameters")
            sys.exit(1)

    # Blowfish cipher needs 8 byte blocks to work with
    def __pad_file(self, file_buffer):
        pad_bytes = 8 - (len(file_buffer) % 8)                                 
        for i in range(pad_bytes - 1):
            file_buffer += chr(randrange(0, 256))
        # final padding byte; % by 8 to get the number of padding bytes
        bflag = randrange(6, 248)
        bflag -= bflag % 8 - pad_bytes
        file_buffer += chr(bflag)
        return file_buffer

    def __depad_file(self, file_buffer):
        pad_bytes = ord(file_buffer[-1]) % 8
        if not pad_bytes:
            pad_bytes = 8
        return file_buffer[:-pad_bytes]

def argument_parser():
    p = argparse.ArgumentParser()

    # you can either decrypt, encrypt or print the file to stdout
    exclusive_group = p.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument("-e", "--encrypt",
            action="store_true",
            help="encrypt a file",
            dest="encrypt")
    exclusive_group.add_argument("-d", "--decrypt",
            action="store_true",
            help="decrypt a file",
            dest="decrypt")
    exclusive_group.add_argument("-c", "--cat",
            action="store_true",
            help="`cat` file to stdout",
            dest="cat")
    p.add_argument(action="store",
            help="infile outfile",
            nargs='+',
            dest="filelist")

    options = p.parse_args()
    return options, p

def writefile(outfile_name, file_buffer):
    outfile = open(outfile_name, 'wb')
    outfile.write(file_buffer)
    outfile.close()

def erase_key(k):
    """Overwrite and erase a value from memory"""
    key = 'x'*len(k)
    del key


if __name__ == '__main__':

    try:
        options, cli_parser = argument_parser()
    except:
        sys.exit(1)

    # assign input and output filenames to the first and second arguments
    try:
        ifname, ofname = options.filelist[0], options.filelist[1]
    except IndexError:
        if options.cat:
            # we can continue if we just want to print the input file
            ifname = options.filelist[0]
        else:
            cli_parser.print_help()
            cli_parser.exit(status=1)

    if os.path.exists(options.filelist[0]):
        infile = open(ifname, 'rb')
        filebuffer = infile.read()
        infile.close()
    else:
        print("File %s does not exist.\n" % ifname)
        sys.exit(1)

    if options.encrypt:
        key = getpass("Choose a password to encrypt your file: ")
        bfc = BFCipher(key)
        filebuffer = bfc.encrypt(filebuffer)
        writefile(ofname, filebuffer)
    elif options.decrypt:
        key = getpass("Insert the password to decrypt your file: ")
        bfc = BFCipher(key)
        filebuffer = bfc.decrypt(filebuffer)
        writefile(ofname, filebuffer)
    elif options.cat:
        key = getpass("Insert the password to decrypt your file: ")
        bfc = BFCipher(key)
        sys.stdout.write(bfc.decrypt(filebuffer))
    else:
        # wtf?!
        sys.exit(2)

    erase_key(key)
