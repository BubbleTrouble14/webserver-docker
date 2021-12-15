FROM postgres:14
ADD CreateDB.sql /docker-entrypoint-initdb.d/
ADD Currency.sql /docker-entrypoint-initdb.d/
ADD CoinPrice.sql /docker-entrypoint-initdb.d/