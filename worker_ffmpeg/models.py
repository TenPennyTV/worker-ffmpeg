from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime

from collections import namedtuple

meta = MetaData()
transcode_task = Table('transcode_task', meta,
                       Column('id', Integer, primary_key=True),
                       Column('expiry', DateTime),
                       Column('resolution', String),
                       Column('length', Integer),
                       Column('transcode_type', String),
                       Column('user_id', String),
                       Column('video_file', String),
                       Column('in_directory', String),
                       Column('out_directory', String),
                       Column('content_id', Integer),
                       Column('retry_count', Integer),
                       Column('status', Integer),
                       Column('uuid', String)
                       )

TranscodeTask = namedtuple('TranscodeTask', transcode_task.columns.keys())


content_tracks = Table('content_tracks', meta,
                       Column('id', Integer, primary_key=True),
                       Column('content_id', Integer),
                       Column('quality', String),
                       Column('directory', String),
                       Column('file_name', String),
                       Column('content_type', String)
                       )

ContentTrack = namedtuple('ContentTrack', content_tracks.columns.keys())