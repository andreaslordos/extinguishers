from datetime import datetime

def removeDuplicates(nodes):
    '''
    Input: nodes of events with lat and long as well as dates. If date, lat and long
    are all similar, then this is a duplicate event
    '''
    def parseDate(date_str):
        list_date=date_str.split("-")
        return datetime(int(str(list_date[0])),int(str(list_date[1])),int(list_date[2]))
        #The above is a hack to account for leading zeros (e.g. 2014-04-03)

    #Step 1 - create a dictionary of all dates, with a corresponding list of fires that
    #occured that day!
    list_of_dates=[]
    dates_to_nodes={}
    for node in nodes:
        date=parseDate(node.acq_date)

        try:
            dates_to_nodes[date].append(node)
        except:
            dates_to_nodes[date]=[node]

        if date not in list_of_dates:
            list_of_dates.append(date)

    ongoingEvents=[]
    deadEvents=[]
    list_of_dates.sort()
    for date in list_of_dates:
        stillAlive=[]
        for event in dates_to_nodes[date]:
            if ongoingEvents==[] and deadEvents==[]: #edge case
                ongoingEvents.append(event)
            else:
                flag=False
                for ongoingEvent in ongoingEvents:
                    distance=(ongoingEvent.getDistance(event))
                    if distance<5:
                        if ongoingEvent not in stillAlive:
                            stillAlive.append(ongoingEvent)
                        ongoingEvent.severity+=1
                        flag=True #Increased severity, so don't add this as a separate event
                        break
                if flag==False:
                    ongoingEvents.append(event) #New event added
                for thing in ongoingEvents:
                    if thing not in stillAlive:
                        ongoingEvents.remove(thing)
                        deadEvents.append(thing)
    for thing in ongoingEvents:
        deadEvents.append(thing)

    return deadEvents

def calculate_pop_density(lat,long,pop):
    '''
    TODO: Implement
    '''
    raise NotImplementedError
