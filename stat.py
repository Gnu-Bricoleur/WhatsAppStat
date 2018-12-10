# -*- coding: utf-8 -*-
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.font_manager as mfm
import matplotlib
import string
import calendar
import numpy as np
import emoji
import regex
import io

font_path = "OpenSansEmoji.ttf"
prop = mfm.FontProperties(fname=font_path)


#courtesy of sheldonzy (https://stackoverflow.com/questions/43146528/how-to-extract-all-the-emojis-from-text)
def countEmoji(text):
	emoji_list = []
	data = regex.findall(r'\X', text)
	for word in data:
		if any(char in emoji.UNICODE_EMOJI for char in word):
			emoji_list.append(word)
	return emoji_list




#one message per line
# day month year hour minute name message
messages = []

with io.open("Discussion.txt", "r", encoding='utf-8') as fichier:
	for line in fichier.readlines():
		try :
			if line[2] == "/" and line [5] == "/":#new message
				day = line[0:2]
				month = line[3:5]
				year = line[6:10]
				hour = line[13:15]
				minute = line[16:18]
				start = line.find('-') + 2
				end = line[start:].find(':') + start
				name = line[start:end]
				message = line[end + 2:]
				messages.append([day, month, year, hour, minute, name, message])
				#print [day, month, year, hour, minute, name, message]
			else:#end of previous message
				messages[-1][6] += line
		except:#end of previous message
			messages[-1][6] += line

#General usage variables
startDiscussion = date(int(messages[0][2]),int(messages[0][1]),int(messages[0][0]))
endDiscussion = date(int(messages[-1][2]),int(messages[-1][1]),int(messages[-1][0]))
durationDiscution = (endDiscussion-startDiscussion).days
users = []
for message in messages:
	if message[5] in users :
		pass
	else:
		users.append(message[5])

ascii_string= """!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ """



#General stats
print "You exchanged " + str(len(messages)) + " messages over the course of " + str(durationDiscution) + " days."
print "That's an average of " + str(len(messages)/durationDiscution) + " messages per day."
lengthFirstSpeaker = []
wordCountFirstSpeaker = []
lengthSecondSpeaker = []
wordCountSecondSpeaker = []
smileyCountFirstSpeaker = 0
smileyCountSecondSpeaker = 0
listeSmiley = []
listeSmileyCount = []
for message in messages:
	if message[5] == users[0]:
		lengthFirstSpeaker.append(len(message[6]))
		wordCountFirstSpeaker.append(len(message[6].split(' ')))
		smileyCountFirstSpeaker += len(countEmoji(message[6]))
	else :
		lengthSecondSpeaker.append(len(message[6]))
		wordCountSecondSpeaker.append(len(message[6].split(' ')))
		smileyCountSecondSpeaker += len(countEmoji(message[6]))
	for smiley in countEmoji(message[6]):
		if smiley in listeSmiley:
			listeSmileyCount[listeSmiley.index(smiley)] += 1
		else:
			listeSmiley.append(smiley)
			listeSmileyCount.append(1)

nbrWord = 0
wordLength = []
for message in messages:
	for word in message[6].split(' '):
		nbrWord += 1
		wordLength.append(len(word))

print "The average message is " + str((sum(lengthFirstSpeaker)+sum(lengthSecondSpeaker))/(len(lengthFirstSpeaker)+len(lengthSecondSpeaker))) \
+ " characters long with an average " + str(sum(lengthFirstSpeaker)/len(lengthFirstSpeaker)) + " characters long message for " + str(users[0]) + \
" and " + str(sum(lengthSecondSpeaker)/len(lengthSecondSpeaker)) + " characters long for " + str(users[1])

print "Thats a grand total of " + str(sum(lengthFirstSpeaker)+sum(lengthSecondSpeaker)) + " characters exchanged. If we admit that we type around 3 characters per second"\
+ "and we read around 300 words per minutes, taking into account that, in this discussion, the average word is " + str(sum(wordLength)/len(wordLength)) + " characters long."\
+ "it means that " + users[0] + " spent " + str(int(sum(lengthSecondSpeaker)/300/(sum(wordLength)/len(wordLength)))+int(sum(lengthFirstSpeaker)/3/60)) + "minutes in this conversation, (" + str(int(sum(lengthFirstSpeaker)/3/60)) + " minutes typing and " + str(int(sum(lengthSecondSpeaker)/300/(sum(wordLength)/len(wordLength)))) +" minutes reading)"\
+ "that's an average of " + str((int(sum(lengthSecondSpeaker)/300/(sum(wordLength)/len(wordLength)))+int(sum(lengthFirstSpeaker)/3/60))/durationDiscution) + " minutes per day."\
+ " and it means that " + users[1] + " spent " + str(int(sum(lengthFirstSpeaker)/300/(sum(wordLength)/len(wordLength)))+int(sum(lengthSecondSpeaker)/3/60)) + "minutes in this conversation, (" + str(int(sum(lengthSecondSpeaker)/3/60)) + " minutes typing and " + str(int(sum(lengthFirstSpeaker)/300/(sum(wordLength)/len(wordLength)))) +" minutes reading)"\
+ "that's an average of " + str((int(sum(lengthFirstSpeaker)/300/(sum(wordLength)/len(wordLength)))+int(sum(lengthSecondSpeaker)/3/60))/durationDiscution) + " minutes per day."


print str(smileyCountFirstSpeaker + smileyCountSecondSpeaker) + " smileys have been used in this conversation (" + str(smileyCountFirstSpeaker) +\
" smileys for " + str(users[0]) + " and " + str(smileyCountSecondSpeaker) + " smileys for " + str(users[1]) + ")"\
+ " that's an average " + str((smileyCountFirstSpeaker + smileyCountSecondSpeaker)/float(len(messages))) + " smiley per message"







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
plt.ylabel("coucou",  fontproperties=prop)
plt.savefig('results/4.png')
plt.show()


#Which smiley is favourite ?
objects = listeSmiley
y_pos = range(len(objects))
performance = listeSmileyCount
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects, rotation='vertical', fontproperties=prop)
plt.ylabel('number of use')
plt.title('Which smiley is more used ?')
#plt.savefig('results/5.png')
plt.show()


