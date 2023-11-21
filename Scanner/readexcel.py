import openpyxl
import socket
import nmap
import concurrent.futures
nmScan = nmap.PortScanner()
path = "sample_ip.xlsx"
workbook = openpyxl.load_workbook(path)
sheet = workbook.active

TYPE=True
def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.error as e:
        print(f"Can't solve ip from domain {domain}")
        return None
    
def scanner_port(host):
    nmScan.scan(f"{host}", arguments='-T4 --top-ports=1000 -Pn')
    hostname =""
    ports=""
    try: 
        for host in nmScan.all_hosts():
            hostname =  nmScan[host].hostname()
            print('\nHost : %s (%s)' % (host,hostname))
            print('State : %s' % nmScan[host].state())
        for proto in nmScan[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)
            ports = nmScan[host][proto].keys()
    except:
        pass
    return hostname, ports

def read_excel(path, pos):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    column_A_values = [cell.value for cell in sheet[pos]]
    workbook.close()
    return column_A_values

def write_excel(workbook, pos, value):
    sheet = workbook.active
    sheet[pos] = value

def scanner(domain):
    value= get_ip_address(domain)
    return value
def process_row(row):
    row_number, cell = row
    if cell is not None:
        if TYPE is True:
            ip = scanner(cell)
        else: 
            ip = cell.strip()
        if ip is not None:
            if TYPE is True:
                sheet[f"B{row_number + 1}"] = ip
                workbook.save(path)
            hostname, ports = scanner_port(ip)
            print(hostname, ports)
            sheet[f"C{row_number + 1}"] = hostname
            sheet[f"D{row_number + 1}"] = str(ports)[11:-2]
        else:
            sheet[f"B{row_number + 1}"] = ""
        workbook.save(path)
    pass
    
def process_row_wrapper(row):
    try:  
        process_row(row)
    except Exception as e:
        print(f"Error processing row: {row}. Error: {e}")


def main():
    if TYPE is True:
        data = read_excel(path= path, pos="A")
    else: 
        data = read_excel(path= path, pos="B")
    num_workers = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(process_row_wrapper, enumerate(data))
    workbook.save(path)
    workbook.close()
    pass
if __name__=="__main__":
    main()