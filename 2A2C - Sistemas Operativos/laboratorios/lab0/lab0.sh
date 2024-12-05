# Ej_1
cat /proc/cpuinfo | grep 'model name' | uniq

# Ej_2
cat /proc/cpuinfo | grep 'model name' | wc -l

# Ej_3
curl -s https://raw.githubusercontent.com/dariomalchiodi/superhero-datascience/master/content/data/heroes.csv | cut -d ';' -f 2 | tr '[:upper:]' '[:lower:]' | tr -d ' ' | grep -v '^$'

# Ej_4
sort -nk5 weather_cordoba.in | head -n 1 | awk '{print $3" "$2" "$1}' ; sort -nk6 weather_cordoba.in | head -n 1 | awk '{print $3" "$2" "$1}' 

# Ej_5
sort -nk3 atpplayers.in

# Ej_6
awk '{print $0, ($7-$8)}' superliga.in | sort -k2,2nr -k9,9nr

# Ej_7
ip link show | grep -o -P -m1 'ether \K(\w|:)+'

# Ej_8_a
mkdir fma && cd fma && for i in $(seq 1 10); do touch "fma_S01E$(printf "%02d" $i)_es.srt"; done 

# Ej_8_b
for chapter in *_es.srt; do mv "$chapter" "${chapter%_es.srt}.srt"; done