
#bash hput.sh 1003 1003-value
key=$1
value=$2

cq_enc=`echo -ne essay: | base64`
key_enc=`echo -ne $key | base64`
value_enc=`echo -ne $value | base64`

data='{ "Row": [ { "key": "'$key_enc'", "Cell": [ { "column": "'$cq_enc'", "$": "'$value_enc'" } ] } ] }'
echo $data
curl -H "Content-Type: application/json" --data "$data" http://192.168.1.24:8890/eev/$key -v
