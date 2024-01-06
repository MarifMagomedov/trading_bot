from environs import Env, load_dotenv
from dataclasses import dataclass


@dataclass
class Config:
    token: str


def load_config():
    env = Env()
    env.read_env()
    return Config(token=env('TOKEN'))
