import os


def get_inoft_vocal_engine_root_path() -> os.path:
    import inoft_vocal_engine
    return os.path.dirname(os.path.abspath(inoft_vocal_engine.__file__))

def get_engine_temp_path() -> os.path:
    return os.path.join(get_inoft_vocal_engine_root_path(), "tmp")
