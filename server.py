#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
    Very simple game with Pygame
"""

import sys, pygame
import os
import time
from pygame.locals import *
import random
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import time,sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# FUNCTIONS *******************
def load_png(name):
    """Load image and return image object"""
    fullname=os.path.join('.',name)
    try:
        image=pygame.image.load(fullname)
        if image.get_alpha is None:
            image=image.convert()
        else:
            image=image.convert_alpha()
    except pygame.error:
        print('Cannot load image: %s' % name)
        raise SystemExit
    return image,image.get_rect()

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.del_client(self)

# SERVER
class MyServer(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.clients = []
        self.run = False
        pygame.init()
        self.screen = pygame.display.set_mode((128, 128))
        print('Server launched')

    def Connected(self, channel, addr):
        self.clients.append(channel)
        print('New connection: %d client(s) connected' % len(self.clients))
        if len(self.clients) == 1:
            self.run = True
            wheels_image, wheels_rect = load_png('Pics/wait1.png')
            self.screen.blit(wheels_image, wheels_rect)

    def del_client(self,channel):
        print('client deconnecte')
        self.clients.remove(channel)

# PROGRAMME INIT
def main_function():
    my_server = MyServer(localaddr = (sys.argv[1],int(sys.argv[2])))
    my_server.launch_game()

if __name__ == '__main__':
    main_function()
    sys.exit(0)