from manim import *
class PracticaFourier(Scene):
    CONFIG={
        'n_vectors': 1,
        'vector_config': {
            'buff': 0,
            'max_tip_length_to_length_ratio': 0.25,
            'max_stroke_width_to_length_ratio': 5,
            'stroke_width': 1.6,
        },
        'center_point': ORIGIN,
        'tex_config': {
            'fill_opacity': 0,
            'stroke_width': 1,
            'stroke_color': WHITE,
        }
    }
    def construct(self):
        path=self.get_path()
        self.add_vectors_circles_path(path)
    def get_path(self):
        square=Square(**self.CONFIG['tex_config'])
        square.set_height(6)
        path=square.family_members_with_points()[0]
        return path
    def add_vectors_circles_path(self,path):
        coefs=self.get_coefficients_of_path(path)
        vectors=self.get_rotating_vectors(coefs)
        self.add(path,vectors)
        self.wait()
    def get_freqs(self):
        n=self.CONFIG['n_vectors']
        all_freqs=list(range(n//2,-n//2,-1))
        all_freqs.sort(key=abs)
        return all_freqs
    def get_coefficients(self):
        return [complex(0) for _ in range(self.CONFIG['n_vectors'])]
    def get_coefficients_of_path(self,path, n_samples=1000, freqs=None):
        if freqs is None:
            freqs=self.get_freqs()
        dt=1/n_samples
        ts=np.arange(0,1,dt)
        samples=np.array([path.point_from_proportion(t) for t in ts])
        samples-=self.CONFIG['center_point']
        complex_samples=samples[:,0]+samples[:,1]*1j
        return [
            np.array([np.exp(-1j*freq*t*TAU)*sample for t, sample in zip(ts, complex_samples)]).sum()*dt for freq in freqs
        ]
    def get_rotating_vectors(self, freqs= None, coefficients= None):
        vectors=VGroup()
        self.center_traker=VectorizedPoint()
        if freqs is None:
            freqs=self.get_freqs()
        if coefficients is None:
            coefficients=self.get_coefficients()
        last_vector=None
        for coef, freq in zip(coefficients, freqs):
            if last_vector is not None:
                center_func=last_vector.get_end()
            else:
                center_func=self.center_traker.get_location()
            vector=self.get_rotating_vector(freq, coef, center_func)
            vector.coef=coef
            vector.freq=freq
            vector.center_func=center_func
            vectors.add(vector)
            last_vector=vector
        return vectors
    def get_rotating_vector(self, freq, coef, center_func):
        vector=Vector(RIGHT, **self.CONFIG['vector_config'])
        vector.scale(abs(coef))
        if abs(coef)==0:
            phase=0
        else:
            phase=np.log(coef).imag
        vector.rotate(phase, about_point=ORIGIN)
        time=0
        phase=np.log(coef).imag
        vector.set_length(abs(coef))
        vector.set_angle(phase+time*freq*TAU)
        vector.shift(center_func-vector.get_start())
        return vector