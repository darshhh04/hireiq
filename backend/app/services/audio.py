from pydub import AudioSegment
from pydub.effects import normalize

CHUNK_MS = 60_000  

def normalize_and_chunk(path: str, out_dir: str) -> list[str]:
    audio = AudioSegment.from_file(path)
    audio = normalize(audio.set_channels(1).set_frame_rate(16000))
    chunk_paths = []
    for i, start in enumerate(range(0, len(audio), CHUNK_MS)):
        chunk_path = f"{out_dir}/chunk_{i}.wav"
        audio[start:start + CHUNK_MS].export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths