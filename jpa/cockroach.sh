CONTAINERID=$(docker run -d -p 26257:26257 -p 8080:8080 cockroachdb/cockroach:v1.0.1 start --insecure)
sleep 2
docker exec -it $CONTAINERID /cockroach/cockroach user set justin --insecure
docker exec -it $CONTAINERID /cockroach/cockroach sql --insecure -e 'CREATE DATABASE test'
docker exec -it $CONTAINERID /cockroach/cockroach sql --insecure -e 'GRANT ALL ON DATABASE test to justin'
docker exec -it $CONTAINERID /cockroach/cockroach sql --insecure -e 'create table test.accounts (id  bigserial not null, balance int not null, first_name string, last_name string, primary key (id))'
docker exec -it $CONTAINERID /cockroach/cockroach sql --insecure -e "INSERT INTO test.accounts (id, balance, first_name, last_name) VALUES (1, 1000, 'stephen', 'harper'), (2, 250, 'justin', 'trudeau')"
