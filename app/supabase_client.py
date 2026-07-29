import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise EnvironmentError(
        "Missing required environment variables: SUPABASE_URL and SUPABASE_ANON_KEY. "
        "Please check your .env file."
    )

# Singleton Supabase client shared across the application
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
