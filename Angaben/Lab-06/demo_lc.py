tx = [10, 20, 30, 40, 50]
logs = ['DEPOSIT: 1000.50', 'DEPOSIT: 2000.50 ', ' DEPOSIT: 3000.50', ' FAILED: 3000.50']

# MAP
double_lc = [tx * 2 for tx in tx]
print(double_lc)
strip_ls = [log.strip() for log in logs]
print(strip_ls)

# FILTER
log_filtered_lc = [log.strip() for log in logs if 'FAILED' in log]
print(log_filtered_lc)
