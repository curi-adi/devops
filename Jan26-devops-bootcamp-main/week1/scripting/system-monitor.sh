# uptime -> show me the load and uptime
# sysetm info -> uname -a /r
# memory usage -> free -h -> %available
# disk usage -> df -h  /workspaces

# cpu -> type of cpu, cpu counts -> lscpu | grep 'Model name\|CPU(s):'

# if i have given a report file 

check_input() {
    if [ ! -f "$1" ] ; then
        echo " provide the report file name"
        exit 1
    fi
}

load() {
    uptime | awk '{ print  $8 $9 $10 }' | awk -F "," '{print $1 }'
}

uptime_info() {
    uptime | awk -F "up " '{ print $2 }' | awk -F "," '{print $1 }'
}


memory_usage_percent() {
    free | awk '/^Mem:/ {printf("%.2f%%\n", $3/$2 * 100.0)}'
}

disk_usage_percent() {
    df -h /workspaces | awk 'NR==2 {print $5}'
}

cpu_info() {
    lscpu | grep 'Model name' | awk -F ": " '{print $2}'
}

generate_report() {
    echo "System Monitor Report" >> "$1"
    echo "=====================" >> "$1"
    echo "Uptime: $(uptime_info)" >> "$1"
    echo "Load Average: $(load)" >> "$1"
    echo "Memory Usage: $(memory_usage_percent)" >> "$1"
    echo "Disk Usage (/workspaces): $(disk_usage_percent)" >> "$1"
    echo "CPU Info: $(cpu_info)" >> "$1"
}
   

main() {
    check_input "$1"
    generate_report "$1"
    echo "System monitor report generated in $1"
}

# calling the function
main "$1"