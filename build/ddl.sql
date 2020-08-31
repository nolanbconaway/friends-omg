
create table {table_name} (
    episode_id varchar not null,
    character_name varchar not null,
    episode_line_number integer not null,
    line_text varchar not null
);

create unique index {table_name}_uidx on {table_name}(episode_id, episode_line_number);
create index {table_name}_line_idx on {table_name}(line_text collate nocase)