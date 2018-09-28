from datetime import datetime

def removeDuplicates(nodes):
    MIN_DISTANCE=3
    '''
    Input: nodes of events with lat and long as well as dates. If date, lat and long
    are all similar, then this is a duplicate event
    '''
    def parseDate(date_str):
        list_date=date_str.split("-")
        return datetime(int(str(list_date[0])),int(str(list_date[1])),int(list_date[2]))
        #The above is a hack to account for leading zeros (e.g. 2014-04-03)
        #Year, month, day

    list_of_dates=[]
    dates_to_nodes={}
    for node in nodes:
        date=parseDate(node.acq_date)
        try:
            dates_to_nodes[date].append(node)
        except:
            dates_to_nodes[date]=[node]

        if date not in list_of_dates:
            list_of_dates.append(date) #Maybe it's not wise to include
                                        #just the date of fires!

    current_events={} #current_fires={(lat,long)=(node,updated)}
    dead_events=[]
    for date in list_of_dates:
        for event in dates_to_nodes[date]:
            updatedThisEvent=False
            for key in current_events:
                distance=current_events[key][0].getDistance(event)
                if distance<MIN_DISTANCE:
                    current_events[key][-1]=True
                    current_events[key][0].severity+=1
                    updatedThisEvent=True
            if updatedThisEvent==False:
                current_events[(event.lat,event.long)]=[event,True]

            x=0
            keys=[]
            for key in current_events:
                keys.append(key)
            while x<len(current_events):
                if current_events[keys[x]][-1]==False:
                    dead_events.append(current_events[keys[x]][0])
                    del current_events[keys[x]]
                    keys.pop(x)
                    x-=1
                x+=1


            for thing in current_events:
                current_events[thing][-1]=False
    return dead_events

def calculate_pop_density(lat,long,pop):
    '''
    TODO: Implement
    '''
    raise NotImplementedError
