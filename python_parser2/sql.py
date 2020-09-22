sql_create_links_table = ''' CREATE TABLE IF NOT EXISTS links (
    id integer PRIMARY KEY,
    path text NOT NULL,
    domain text,
    protocol text
) '''
sql_create_words_table = ''' CREATE TABLE IF NOT EXISTS words (
    id integer PRIMARY KEY,
    word text NOT NULL,
    rat integer NOT NULL,
    link integer NOT NULL,
    FOREIGN KEY (link) REFERENCES links(id)
) '''