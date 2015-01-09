
echo ''
echo 'Checking Elasticsearch / mongodb / redis processes..'
echo ''

ps aux | grep '[e]lasticsearch' && echo 'Elasticsearch is running.'
ps aux | grep '[m]ongod' && echo 'Mongodb is running.'
ps aux | grep '[r]edis' && echo 'Redis is running.'

