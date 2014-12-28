
echo 'Checking Elasticsearch and mongodb processes..'

ps aux | grep '[e]lasticsearch' && echo 'Elasticsearch is running.'
ps aux | grep '[m]ongod' && echo 'Mongodb is running.'

