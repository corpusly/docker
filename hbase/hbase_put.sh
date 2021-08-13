
#bash hbase_put.sh eev essay test 1002 1002-value

table=$1
cf=$2
column=$3
key=$4
value=$5

cq_enc=`echo -ne $cf:$column | base64`

key_enc=`echo -ne $key | base64`
value_enc=`echo -ne $value | base64`

data='{ "Row": [ { "key": "'$key_enc'", "Cell": [ { "column": "'$cq_enc'", "$": "'$value_enc'" } ] } ] }'
echo $data
curl -H "Content-Type: application/json" --data "$data" http://192.168.1.24:8890/$table/$key -v
