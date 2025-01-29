#These 4 imports below are for the e-mail sending process.
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

#These 2 imports below are for timestamp calculation (additional)
from java.lang import System
from datetime import datetime

# User-defined parameters
my_server = sys.argv[1]
#You pass the server's ip address or simply pass "localhost" is it's running locally on your machine.

username = 'weblogic'
password = 'Princeofpersi@55'
#(((((CHANGE THIS INFO ABOVE)))))

url = 't3://%s:7001' % (my_server)

#(((Path of the html report)))
html_file_path= "C:\\Users\\ahmed\\Desktop\\send_me.html"


# Connect to WebLogic server
try:
    connect(username, password, url)
except Exception, e:
    print "Connection failed! Make sure the server is up or double check your credentials."

#----------------------------------------
# Report Server Status
#----------------------------------------

# Open HTML file for writing
try:
    html_file = open(html_file_path, "w+")
except Exception, e:
    print "Can't open the file due to this error:\n" + str(e)

# (((((CHANGE THIS PATH ABOVE || That's the html file that we gonna send)))))

rowColor= "#f7f7f7"
html_file.write('<html>')
html_file.write('<head>')
    #styles
html_file.write('<style>')
html_file.write('.reportBody { color: white; background: linear-gradient(to right, #3a6186, #89253e); text-align: center; font-size: 1.4rem}')
html_file.write('table { min-width: 50%; margin: auto; background-color: #f7f7f7; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); border: 1px solid black; text-align: center; padding: 2px; font-size: 1.2rem; color: #000; border-collapse: collapse;}')
html_file.write('td, th { border: 1px solid black; min-width: 60px; min-height: 40px; padding: 3px;}')  # Ensure all cell borders are black
html_file.write('.table-header { background-color: #6ea8fe; color: black;}')
html_file.write('</style>')
html_file.write('</head>')

    #Starting Page Body
html_file.write('<body class="reportBody" style="color: white;">')
# html_file.write('<b>yellow</b>')
# html_file.write('<b>red</b>')
html_file.write('<h2 style="color: rgb(80, 199, 122);">[INFORMATIVE] WebLogic Environment Status</h2>')
html_file.write('<h3 style="color: white;">SERVER STATUS REPORT: ' + url + '</h3>')
html_file.write('<table class="table1">')
html_file.write('<tr class="table-header"><th>Server Name</th><th>Status</th><th>Health</th></tr>')

# Extract server names and runtime information
domainRuntime()
serverRuntimes = domainRuntimeService.getServerRuntimes()

def healthstat(server_name):
    cd('/ServerRuntimes/' + server_name + '/ThreadPoolRuntime/ThreadPoolRuntime')
    s = get('HealthState')
    return s.toString().split(',')[2].split(':')[1].split('HEALTH_')[1]

for server in serverRuntimes:
    server_name = server.getName()
    status = str(server.getState())
    health = healthstat(server_name)
    
    # Determine health color
    if health == 'OK':
        healthColor = 'green'
    elif health == 'WARN':
        healthColor = 'yellow'
    else:
        healthColor = 'red'

    
    # Write row to HTML
    html_file.write('<tr>')
    html_file.write('<td>%s</td>'%(server_name))
    html_file.write('<td>%s</td>' %(status))
    html_file.write('<td style="background-color: %s;">%s</td>' % (healthColor, health))
    html_file.write('</tr>')

html_file.write('</table>')
html_file.write('<br><br>')

#----------------------------------------
# Report Heap Details
#----------------------------------------
# Definition to print a running server's heap details
html_file.write('<table class="table2">')
html_file.write('<tr class="table-header"><th>Managed Server</th><th>HeapFreeCurrent</th><th>HeapSizeCurrent</th><th>HeapFreePercent</th></tr>')

def printHeapDetails(server_name, rowColor):
    domainRuntime()
    cd('/')
    cd('ServerRuntimes/' + server_name + '/JVMRuntime/' + server_name)

    #get() returns the size in bytes, so we need to divide by 1024 to turn them to kilobytes.
    #We divide by 1024 again to turn them to migabytes
    #Dividying by 1024 twice is like dividying by 1024^2
    hf = round((float(get('HeapFreeCurrent')) / (1024 * 1024)), 2)  # Convert to MB
    hs = round((float(get('HeapSizeCurrent')) / (1024 * 1024)), 2)  # Convert to MB
    hfpct = float(get('HeapFreePercent'))

    # Determine cell color for HeapFreePercent
    if hfpct <= 10:
        cellcolor = 'red'
    elif hfpct <= 20:
        cellcolor = 'yellow'
    else:
        cellcolor = rowColor


    # Write row to HTML
    html_file.write('<tr style="background-color: %s;">' % rowColor)
    html_file.write('<td>%s</td>' % server_name)
    html_file.write('<td>%s MB</td>' % hf)
    html_file.write('<td>%s MB</td>' % hs)
    html_file.write('<td style="background-color: %s;">%s%%</td>' % (cellcolor, hfpct)) #We use %% to escape the '%' and print it like any normal text.
    html_file.write('</tr>')


for server in serverRuntimes:
    printHeapDetails(server.getName(), rowColor)

html_file.write('</table>')
html_file.write('<br><br>')
#----------------------------------------
# Report JDBC Status
#----------------------------------------

html_file.write('<h3 style="color: white;">SERVER JDBC RUNTIME INFORMATION</h3>')
html_file.write('<table class="table3">')
html_file.write('<tr class="table-header"><th>Data Source</th><th>State</th><th>Active Connections</th><th>Waiting for Connections</th></tr>')

for server in serverRuntimes:
    jdbcRuntime = server.getJDBCServiceRuntime()
    datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans()
    if datasources is None or len(datasources) == 0:
        html_file.write('<tr><td colspan="5">No JDBC data sources available for %s</td></tr>' %(server.getName()))
    else:
        for datasource in datasources:
            # Set colors for different states and metrics
            if datasource.getState() != "Running":
                stateColor = 'red'
            else:
                stateColor = rowColor

            if datasource.getActiveConnectionsCurrentCount() > 20:
                acColor = 'red'
            elif datasource.getActiveConnectionsCurrentCount() > 10:
                acColor = 'yellow'
            else:
                acColor = rowColor

            if datasource.getWaitingForConnectionCurrentCount() > 5:
                wcColor = 'red'
            elif datasource.getWaitingForConnectionCurrentCount() > 2:
                wcColor = 'yellow'
            else:
                wcColor = rowColor


            # Write row to HTML
            html_file.write('<tr>')
            html_file.write('<td>%s</td>' % datasource.getName())
            html_file.write('<td style="background-color: %s;">%s</td>' % (stateColor, datasource.getState()))
            html_file.write('<td style="background-color: %s;">%d</td>' % (acColor, datasource.getActiveConnectionsCurrentCount()))
            html_file.write('<td style="background-color: %s;">%d</td>' % (wcColor, datasource.getWaitingForConnectionCurrentCount()))
            html_file.write('</tr>')

html_file.write('</table>')
html_file.write('<br><br>')

#----------------------------------------
# Report JMS Status
#----------------------------------------
html_file.write('<h3 style="color: white;">SERVER JMS STATUS INFORMATION</h3>')
html_file.write('<table class="table4">')
html_file.write('<tr class="table-header"><th>Server</th><th>JMS Server</th><th>Destination Name</th><th>Destination Type</th><th>Messages Current Count</th><th>Messages High Count</th><th>Consumers Current Count</th><th>Consumers High Count</th><th>Consumers Total Count</th></tr>')

for server in serverRuntimes:
    serverName = server.getName()
    # print("Checking JMS Runtime for Server:", serverName)
    jmsRuntime = server.getJMSRuntime()
    jmsServers = jmsRuntime.getJMSServers()

    if jmsServers is None or len(jmsServers) == 0:
        html_file.write('<tr><td>%s</td><td colspan="8">No JMS Information For %s</td></tr>' % (serverName, serverName))
    else:
        for jmsServer in jmsServers:
            jmsServerName = jmsServer.getName()            
            destinations = jmsServer.getDestinations()
            if destinations is None or len(destinations) == 0:
                #print("rowcolor: %s" %(rowColor))
                html_file.write('<tr><td>%s</td><td>%s</td><td colspan="7">No Destinations for %s</td></tr>' % (serverName, jmsServerName, jmsServerName))
            else:
                for destination in destinations:
                    html_file.write('<tr>')
                    html_file.write('<td>%s</td>' % serverName)
                    html_file.write('<td>%s</td>' % jmsServerName)
                    html_file.write('<td>%s</td>' % destination.getName())
                    html_file.write('<td>%s</td>' % destination.getDestinationType())
                    html_file.write('<td>%d</td>' % destination.getMessagesCurrentCount())
                    html_file.write('<td>%d</td>' % destination.getMessagesHighCount())
                    html_file.write('<td>%d</td>' % destination.getConsumersCurrentCount())
                    html_file.write('<td>%d</td>' % destination.getConsumersHighCount())
                    html_file.write('<td>%d</td>' % destination.getConsumersTotalCount())
                    html_file.write('</tr>')
html_file.write('</table>')
html_file.write('<br><br>')
html_file.write('<h4 style="color: white;">**************** END OF REPORT ****************</h4>')


# Get the current timestamp in milliseconds
current_timestamp_ms = System.currentTimeMillis()
# Convert to a Python datetime object and then to a human-readable time
human_readable_time = datetime.fromtimestamp(current_timestamp_ms / 1000.0).strftime('%Y-%m-%d %H:%M')


html_file.write('<b style="color: white;">This report was created in: %s</b>' % human_readable_time)
html_file.write('</body>')
html_file.write('</html>')

# Reset pointer to the beginning for reading (I can close and reopen the file instead actually, but this approach causes less processing)
html_file.seek(0)
file_content= html_file.read()
html_file.close()

#When it's "informative", the color isn't strictly "green", that's why I used the rgb() function to pick a better looking color.
informative = '<h2 style="color: rgb(80, 199, 122);">[INFORMATIVE] WebLogic Environment Status</h2>'
warning = '<h2 style="color: yellow;">[WARNING] WebLogic Environment Status</h2>'
critical = '<h2 style="color: red;">[CRITICAL] WebLogic Environment Status</h2>'

if 'red' in file_content:
    updated_content= file_content.replace(informative, critical)
    html_file= open(html_file_path, "w")
    html_file.write(updated_content)
    html_file.close()
elif 'yellow' in file_content:
    updated_content= file_content.replace(informative, warning)
    html_file= open(html_file_path, "w")
    html_file.write(updated_content)
    html_file.close()

#disconnect from the server
disconnect()


#----------------------------------------
# Sending the report
#----------------------------------------
sender_email = "anamainyas5@gmail.com"
app_pwd= 'smnk jott qxcx zyff'
receiver_email = "yosrym238@gmail.com"
subject = "Weblogic Status Report"
file= open(html_file_path, 'r')
#(((Change this information above)))

content= file.read()
if "red" in content:
    alert_code= '[CRITICAL]'
elif "yellow" in content:
    alert_code= '[WARNING]'
elif "green" in content:
    alert_code= "[INFORMATIVE]"
#The if else statement above is to change the report subject's color based on the general status of the report

subject= alert_code + ' ' + subject

# Set up the MIME
message = MIMEMultipart()                   #This method returns a partitioned email object 
message['From'] = sender_email              #Fill email's "From" field
message['To'] = receiver_email              #Fill email's "To" field
message['Subject'] = subject                #Fill email's "Subject" field
message.attach(MIMEText(content, 'html'))   #The attach() method is used to add additional parts to the body of the email
                                            #In this case, we're adding the html report.

# Connect to Gmail's SMTP server and send email
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Upgrade to a secure connection
    server.login(sender_email, app_pwd)
    server.sendmail(sender_email, receiver_email, message.as_string())
    print "Email sent successfully!"
except Exception, e:
    print "Error sending the email:\n" + str(e)  # Use .format for compatibility
finally:
    server.quit()  # Ensure the connection is closed

file.close()
#----------------------------------------
# Exit WLST
#----------------------------------------
exit()

#::NOTE::
#ONLY CHANGE THE RECEIVING EMAIL TO YOURS AND RUN THE SCRIPT TO MAKE SURE THAT IT'S WORKING
#After that, you create an app password of your own from the email that will send the email.
#Note that that account must have 2FA enabled to be able to create an app password.