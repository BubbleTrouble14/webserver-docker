FROM postgres:14
ADD CreateChiaTables.sql /docker-entrypoint-initdb.d/
ADD CreateExchangeRateTable.sql /docker-entrypoint-initdb.d/
ADD CreateCoinPriceTable.sql /docker-entrypoint-initdb.d/