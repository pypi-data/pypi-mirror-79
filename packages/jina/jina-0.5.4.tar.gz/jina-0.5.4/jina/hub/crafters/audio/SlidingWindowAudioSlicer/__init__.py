from typing import Dict, List

import numpy as np
from jina.executors.crafters import BaseSegmenter


class AudioSegmenter(BaseSegmenter):
    """
    :class:`AudioSegmenter` provides the functions for segmenting audio signal.
    .. warning::
        :class:'AudioSegmenter' is intended to be used internally.
    """

    def __init__(self, frame_length: int, hop_length: int, *args, **kwargs):
        """
        :param frame_length: the number of samples in each frame
        :param hop_length: number of samples to advance between frames
        """
        super().__init__(*args, **kwargs)
        self.frame_length = frame_length
        self.hop_length = hop_length

    def segment(self, signal):
        import librosa
        if signal.ndim == 1:  # mono
            frames = librosa.util.frame(signal, frame_length=self.frame_length, hop_length=self.hop_length, axis=0)
        elif signal.ndim == 2:  # stereo
            left_frames = librosa.util.frame(
                signal[0,], frame_length=self.frame_length, hop_length=self.hop_length, axis=0)
            right_frames = librosa.util.frame(
                signal[1,], frame_length=self.frame_length, hop_length=self.hop_length, axis=0)
            frames = np.concatenate((left_frames, right_frames), axis=0)
        else:
            raise ValueError(f'audio signal must be 1D or 2D array: {signal}')
        return frames


class SlidingWindowAudioSlicer(AudioSegmenter):
    """
    :class:`SlidingWindowAudioSlicer` segments the audio signal on the doc-level into frames on the chunk-level with a
    sliding window.
    """

    def __init__(self, frame_size: int, frame_overlap_size: int, *args, **kwargs):
        """
        :param frame_size: the number of samples in each frame
        :param frame_overlap_size: the number of samples each frame overlaps its previous frame
        """
        hop_size = frame_size - frame_overlap_size
        assert hop_size > 0, 'frame_overlap_size must be smaller than frame_size'
        super().__init__(frame_size, hop_size, *args, **kwargs)

    def craft(self, blob: 'np.ndarray', *args, **kwargs) -> List[Dict]:
        """
        Slices the input audio signal array into frames with a sliding window and saves the `ndarray` of each frame in
        the `blob` of each Chunk.

        :param blob: the ndarray of the audio signal
        :return: a list of Chunk dicts with audio frames
        """
        frames = self.segment(blob)

        return [dict(offset=idx, weight=1.0, blob=frame, length=frames.shape[0])
                for idx, frame in enumerate(frames)]
