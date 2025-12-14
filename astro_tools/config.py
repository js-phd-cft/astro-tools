from dotenv import load_dotenv

def astro_tools_load_env(env_file='.env'):
    """
    Optional: Load .env file into os.environ.
    Not required - users can manage env vars themselves.
    """
    load_dotenv(env_file)