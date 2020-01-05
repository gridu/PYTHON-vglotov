import argparse

PARSER = argparse.ArgumentParser()

PARSER.add_argument('--port', type=int, default=5000, help='Port number')
PARSER.add_argument('--log_method', type=str, default='console', help='Logging method')
PARSER.add_argument('--log_lvl', type=str, default='INFO', help='Logging level')
PARSER.add_argument('--db_path', type=str, default='///', help='Path to database')
PARSER.add_argument('--db_name', type=str, default='book_db.db', help='Database name to be')

ARGS = PARSER.parse_args()

port = ARGS.port
log_method = ARGS.log_method
log_lvl = ARGS.log_lvl
db_path = ARGS.db_path
db_name = ARGS.db_name
