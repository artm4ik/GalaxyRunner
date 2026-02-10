import subprocess
import threading
import os
import arcade
from pathlib import Path


def resolve_sound_path(resource_path: str) -> str:
    path = arcade.resources.resolve_resource_path(resource_path)
    return str(path.absolute())


class SoundManager:

    def __init__(self):
        self.sounds = {}

    def register(self, name: str, resource_path: str):
        try:
            full_path = resolve_sound_path(resource_path)
            if os.path.exists(full_path):
                self.sounds[name] = full_path
            else:
                print(f"Warning: Sound file not found: {full_path}")
        except Exception as e:
            print(f"Error resolving sound {name}: {e}")

    def play(self, name: str):
        path = self.sounds.get(name)
        if not path:
            return
        
        # Запускаем в отдельном потоке, чтобы не тормозить игру
        thread = threading.Thread(target=self._play_file, args=(path,), daemon=True)
        thread.start()

    @staticmethod
    def _play_file(path: str):
        try:
            # -v 0.5 ставит громкость 50% чтобы не оглушить
            # -t 1 ограничивает время воспроизведения 1 секундой (для коротких звуков)
            subprocess.run(
                ["afplay", "-v", "0.5", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass
