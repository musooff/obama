from SimpleAudioIndexer import SimpleAudioIndexer as sai

indexer = sai(mode="cmu", src_dir="sai", )

indexer.index_audio()
print indexer.get_timestamps()
