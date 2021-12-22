# Felipe Pazos
# 12/16/2021
# Script to generate a schematic of marimba key layout.

import csv
import pyglet

import marimba_keys_helpers
import pyglet_handler

def main():
    accs = marimba_keys_helpers.get_accidentals()
    nats = marimba_keys_helpers.get_naturals()
    
    marimba_keys_helpers.set_nodes('natural_nodes.csv', nats)
    marimba_keys_helpers.set_nodes('accidental_nodes.csv', accs)
    
    all_keys = accs | nats
    
    marimba_keys_helpers.set_x_bounds(nats, accs)
    marimba_keys_helpers.set_y_bounds(nats, accs)
    pyglet_handler.set_keys(nats, accs)

    pyglet_handler.create_midpoint()
    pyglet_handler.create_bounds()
    pyglet_handler.create_keys()
    lines = marimba_keys_helpers.get_best_fit_lines(nats, accs)
    pyglet_handler.create_nodelines(lines)
    pyglet_handler.create_leftbutt()
    pyglet_handler.create_rightbutt()
    pyglet_handler.run()


main()