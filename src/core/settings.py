from pydantic_settings import BaseSettings, SettingsConfigDict

class MinioSettings(BaseSettings):
    minio_host: str
    minio_port: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

minio_settings = MinioSettings()


class SftpSettings(BaseSettings):
    sftp_host: str
    sftp_port: int
    sftpuser: str
    sftppassword: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

sftp_settings = SftpSettings()


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_debug: bool

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()


class DBSettings(BaseSettings):
    db_url: str = f'postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}'
    db_debug: bool = settings.postgres_debug


db_settings = DBSettings()


class RedisSettings(BaseSettings):
    redis_host: str
    redis_user: str
    redis_password: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

redis_settings = RedisSettings()


class RabbitSettings(BaseSettings):
    rabbit_host: str
    rabbit_user: str
    rabbit_password: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

rabbit_settings = RabbitSettings()
