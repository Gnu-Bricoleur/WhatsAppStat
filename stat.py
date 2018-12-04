from datetime import date
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import string
import calendar
import numpy as np

#one message per line
# day month year hour minute name message
messages = []

with open("Discussion.txt", "r") as fichier:
	for line in fichier.readlines():
		try :
			if line[2] == "/" and line [5] == "/":#new message
				day = line[0:2]
				month = line[3:5]
				year = line[6:10]
				hour = line[14:16]
				minute = line[17:19]
				start = line.find('-') + 2
				end = line[start:].find(':') + start
				name = line[start:end]
				message = line[end + 2:]
				messages.append([day, month, year, hour, minute, name, message])
			else:#end of previous message
				messages[-1][6] += line
		except:#end of previous message
			messages[-1][6] += line

startDiscussion = date(int(messages[0][2]),int(messages[0][1]),int(messages[0][0]))
endDiscussion = date(int(messages[-1][2]),int(messages[-1][1]),int(messages[-1][0]))
durationDiscution = (endDiscussion-startDiscussion).days

#General stats
print "You exchanged " + str(len(messages)) + " messages over the course of " + str(durationDiscution) + " days."
print "That's an average of " + str(len(messages)/durationDiscution) + " messages per day."

#Graphs
#Who send more messages ?
firstSpeaker = messages[0][5]
firstSpeakerMessages = 0
secondSpeakerMessages = 0
for message in messages:
	if message[5] == firstSpeaker:
		firstSpeakerMessages += 1
	else:
		secondSpeakerMessages += 1
		secondSpeaker = message[5]

labels = firstSpeaker, secondSpeaker
sizes = [firstSpeakerMessages, secondSpeakerMessages]
colors = ['pink', 'lightskyblue']
explode = (0.1, 0)  # explode 1st slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.title('Who send more messages ?')
plt.savefig('results/1.png')
plt.show()


#When are the messages sent ? (1 - full period)
dateMessage = []
nbrMessage = [1]
dateMessage.append(str(messages[0][0])+"/"+str(messages[0][1])+"/"+str(messages[0][2]))
for message in messages:
	if dateMessage[-1] == str(message[0])+"/"+str(message[1])+"/"+str(message[2]):
		nbrMessage[-1] += 1
	else:
		dateMessage.append(str(message[0])+"/"+str(message[1])+"/"+str(message[2]))
		nbrMessage.append(1)
objects = dateMessage
y_pos = range(len(objects))
performance = nbrMessage
average = [len(messages)/len(objects)]*len(objects)
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects, rotation='vertical')
plt.ylabel('Messages per day')
plt.title('When are the messages sent ?')
plt.plot(y_pos, average, color='pink', label='Average')
plt.savefig('results/2.png')
plt.show()


#When are the messages sent ? (1 - week)
dayMessage = [0]*7
for message in messages:
	dayMessage[calendar.weekday(int(message[2]), int(message[1]), int(message[0]))] += 1

objects = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
y_pos = range(len(objects))
performance = dayMessage
average = [len(messages)/len(objects)]*len(objects)
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects, rotation='vertical')
plt.ylabel('Messages per day')
plt.title('When are the messages sent ?')
plt.plot(y_pos, average, color='pink', label='Average')
plt.savefig('results/3.png')
plt.show()


#When are the messages sent ? (1 - day)
hourMessage = [0]*24
for message in messages:
	hourMessage[int(message[3])] += 1

fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)

N = 24
theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)
radii = hourMessage
width = 2*np.pi/N
bars = ax.bar(theta, radii, width=width, bottom=0.0)

reds = np.arange(0, 255, 255/len(bars))
for bar, red in zip(bars,reds):
	bar.set_facecolor((red/255.0, 0, 1))
plt.title('When are the messages sent ?')
plt.savefig('results/4.png')
plt.show()



