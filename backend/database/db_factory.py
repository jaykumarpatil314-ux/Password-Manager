from database.base_repository import BaseRepository
from database.postgres_repository import PostgresRepository
from database.mongodb_repository import MongoRepository

def get_repository(config) -> BaseRepository:
    """
    Factory function to get the appropriate database repository
    based on configuration
    """
    db_type = config.DATABASE_TYPE.lower()
    
    if db_type == 'postgresql':
        repo = PostgresRepository(config.POSTGRES_URI)
        print(f"Using PostgreSQL database")
    elif db_type == 'mongodb':
        repo = MongoRepository(config.MONGODB_URI)
        print(f"Using MongoDB database")
    else:
        raise ValueError(f"Unsupported database type: {db_type}. Use 'postgresql' or 'mongodb'")
    
    repo.initialize()
    return repo
