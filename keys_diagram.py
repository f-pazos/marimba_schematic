# Felipe Pazos
# 12/16/2021
# Script to generate a schematic of marimba key layout.

import csv
import pyglet

import key_data
import pyglet_handler

def main():
    accs = key_data.get_accidentals()
    nats = key_data.get_naturals()
    
    key_data.set_nodes('natural_nodes.csv', nats)
    key_data.set_nodes('accidental_nodes.csv', accs)
    
    all_keys = accs | nats
    
    key_data.set_x_bounds(nats, accs)
    key_data.set_y_bounds(nats, accs)
    pyglet_handler.set_keys(nats, accs)

    pyglet_handler.create_midpoint()
    pyglet_handler.create_bounds()
    pyglet_handler.create_keys()
    lines = key_data.get_best_fit_lines(nats, accs)
    pyglet_handler.create_nodelines(lines)
    pyglet_handler.create_leftbutt()
    pyglet_handler.create_rightbutt()
    pyglet_handler.run()


main()