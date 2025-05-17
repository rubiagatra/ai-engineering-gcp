CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings (
    show_id TEXT NOT NULL,
    season_number INTEGER NOT NULL,
    episode_id INTEGER NOT NULL,
    chunk TEXT,
    embedding vector(768),
    PRIMARY KEY (show_id, season_number, episode_id)
);

INSERT INTO embeddings (show_id, season_number, episode_id, chunk) VALUES
 ('Kehidupan', 1,  1,  'Natasha mengakui cintanya pada Budi.'),
 ('Kehidupan', 1,  2,  'Budi dan Natasha bertunangan.'),
 ('Kehidupan', 1,  3,  'Marni dan Hendra bercerai.'),
 ('Sahabat Terbaik', 1,  1,  'Astri mengakui cintanya pada Rio.'),
 ('Sahabat Terbaik', 1,  2,  'Rio dan Astri bertunangan.'),
 ('Sahabat Terbaik', 1,  3,  'Bayu dan Putri bercerai.')
;
