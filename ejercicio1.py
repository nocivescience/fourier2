from manim import *
import itertools as it
class Caso1Scene(Scene):
    CONFIG={
            'n_vectors': 12,
            'vector_config': {
                'buff': 0,
                'max_tip_length_to_length_ratio': 0.25,
                'max_stroke_width_to_length_ratio': 10,
                'stroke_width': 1.6,
                'tip_length': 0.15,    
            },
            'time': 0,
        }
    def construct(self):
        vectors=self.get_rotating_vectors()
        vectors[0].set_opacity(0)
        self.add(vectors)
        self.wait(23)
    def get_rotating_vectors(self, freqs= None, coefficients= None):
        vectors=VGroup()
        if freqs is None:
            freqs=self.get_freqs()
        if coefficients is None:
            coefficients=self.get_coefficients()
        last_vector=None
        for coef, freq  in zip(coefficients, freqs):
            center_tracker=VectorizedPoint(ORIGIN)
            if last_vector is not None:
                center_func=last_vector.get_end
            else:
                center_func=center_tracker.get_location
            vector=self.get_rotating_vector(freq, coef,center_func)
            vectors.add(vector)
            last_vector=vector
        return vectors
    def get_rotating_vector(self, coefficient, freq, center_func):
        vector=Vector(RIGHT,**self.CONFIG['vector_config'])
        vector.center_func=center_func
        vector.coef=coefficient
        vector.freq=freq
        vector.scale(coefficient/5)
        vector.set_angle((freq))
        vector.shift(center_func()-vector.get_start())
        vector.add_updater(self.update_vector)
        return vector
    def get_freqs(self):
        n=self.CONFIG['n_vectors']
        all_freqs=[i for i in range(self.CONFIG['n_vectors'])]
        all_freqs.sort(key=abs)
        return all_freqs
    def get_coefficients(self):
        return [i for i in range(self.CONFIG['n_vectors'])]
    def update_vector(self, vector, dt):
        self.CONFIG['time']+=dt
        vector.rotate(self.CONFIG['time']/180)
        vector.shift(vector.center_func()-vector.get_start())
        return vector
