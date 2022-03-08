# Covidinfo_chatbot_project 🦠

This is a project for creating a telegram chatbot offering the real-time COVID Information🦠 to the users.<br />
In this version, the information is only confined to 'South Korea COVID' related info.<br /> 
There are 3 things you can get by talking to this chatbot as below:<br />
1) Today's new COVID case in South Korea<br />
2) Recent News (headlines and direct links to article) with keyword 'south korea covid'<br />
3) Images related to COVID (with keyword: how to fight covid)<br />

Methodology:<br />
I created 3 types of crawler mainly using beautifulsoup:<br />
- Crawler for the number of today's new covid case (in South Korea)<br />
- Crawler for the recent news related to South Korea Covid<br />
- Crawler for related images with keyword 'how to fight covid'<br />

And then, I created handler that contains the response messages of chatbot based on user's input.<br />
*Just FYI, you need to put your own chatbot's api token key and chat_id in your code to recreate your own bots using this repository's code.*

**Test video - Chatbot mobile version**
<video src="https://user-images.githubusercontent.com/53321802/157106147-750aab08-91a7-4546-b2c5-55fa08c1b9ea.MP4"></video>

**Test video - Chatbot PC version**
<video src="https://user-images.githubusercontent.com/53321802/157106157-afd46d4a-d04d-4431-aa01-38bf280b4304.mov"></video>
