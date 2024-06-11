import sys
import math

import pygame as pg
import moderngl as mgl

from array import array

from settings import *

class ShaderArt():
    def __init__(self):
        pg.init()
        
        self.is_running = True

        self.screen = pg.display.set_mode(WIN_RES, pg.OPENGL | pg.DOUBLEBUF)
        self.display = pg.Surface(WIN_RES)
        self.ctx = mgl.create_context()
        
        self.initialize_shaders()
        
        
    def initialize_shaders(self) -> None:
        quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # top left
            1.0, 1.0, 1.0, 0.0,   # top right
            -1.0, -1.0, 0.0, 1.0, # bottom left
            1.0, -1.0, 1.0, 1.0   # bottom right
        ]))
        
        self.vert_shader, self.frag_shader = self.get_shaders('tutorial')
        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])
        
        
    def get_shaders(self, shader_name: str) -> str:
        with open (f'./shaders/{shader_name}/{shader_name}.vert', 'r') as file:
            vert_shader = file.read()
            file.close()

        with open (f'./shaders/{shader_name}/{shader_name}.frag', 'r') as file:
            frag_shader = file.read()
            file.close()

        return vert_shader, frag_shader
    
    
    def get_time(self) -> float:
        return pg.time.get_ticks() / 1000
    
    
    def surf_to_texture(self, surf: pg.surface) -> mgl.Context.texture:
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (mgl.LINEAR, mgl.LINEAR)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
    
    
    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
                pg.quit()
                sys.exit()
                
                
    def uniforms(self):
        ...
        
        
    def render(self) -> None:
        time = self.get_time()

        frame_tex = self.surf_to_texture(self.display)
        frame_tex.use(0)
        
        self.uniforms()
        
        self.render_object.render(mode=mgl.TRIANGLE_STRIP)
        
        pg.display.flip()
        frame_tex.release()
        
        
    def run(self) -> None:
        while self.is_running:
            
            self.handle_events()
            
            self.render()           
            
            
def main():
    app = ShaderArt()
    app.run()
    
    
if __name__ == "__main__":
    main()