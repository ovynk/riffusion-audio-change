import torch

from diffusers import DiffusionPipeline
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from riffusion.spectrogram_params import SpectrogramParams


class Model:

    def __init__(self):
        self.device = None
        self.spectrogram = None

    def __load_pipe(self, device, low_cpu_mem_usage=False):
        self.device = device

        pipe = DiffusionPipeline.from_pretrained(
            "riffusion/riffusion-model-v1",
            low_cpu_mem_usage=low_cpu_mem_usage
        )
        pipe.to(device)
        return pipe

    def txt2spectrogram(self,
                        prompt,
                        negative_prompt=None,
                        audio_duration=5,
                        device='cpu',
                        pipeline_low_cpu_memory_usage=False,
                        guidance_scale=7.0,
                        num_inference_steps=None,
                        seed=1
                        ):
        # 104 is a little bigger than one second
        # it needs to be multiplied by 8 for pipe (so, 100 doesn't work)
        width_duration = (int(audio_duration) + 1) * 104

        pipe = self.__load_pipe(device, pipeline_low_cpu_memory_usage)
        generator = torch.Generator(device=device)
        generator.manual_seed(seed)

        spectrogram = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width_duration,
            guidance_scale=guidance_scale,
            generator=generator,
            # num_inference_steps=num_inference_steps,
        ).images[0]

        self.spectrogram = spectrogram

    def spectrogram2audio(self, use_20khz=False):
        assert self.spectrogram is not None, "Spectrogram is not created."

        if use_20khz:
            spectrogram_params = SpectrogramParams(
                min_frequency=10,
                max_frequency=20000,
                sample_rate=44100,
                stereo=True,
            )
        else:
            spectrogram_params = SpectrogramParams(
                min_frequency=0,
                max_frequency=10000,
                stereo=False,
            )

        converter = SpectrogramImageConverter(spectrogram_params, device=self.device)

        audio = converter.audio_from_spectrogram_image(image=self.spectrogram)
        audio.export('generated_audio.wav', format='wav')
