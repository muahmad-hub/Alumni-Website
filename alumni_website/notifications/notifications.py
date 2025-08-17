from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import random
import threading

# Main parent class for all notifications
class Notification:
    def __init__(self, receiver, sender=None):
        self.receiver = receiver
        if sender is not None:
            self.sender_name = f"{sender.profile.first_name} {sender.profile.last_name}"
        else:
            self.sender_name = None 
        self.receiver_email = receiver.email
        self.from_email = "oryxalumni@gmail.com"

    def get_subject(self):
        raise NotImplementedError
    
    def get_template(self):
        raise NotImplementedError
    
    def get_context(self):
        raise NotImplementedError
    
    def get_text_content(self):
        raise NotImplementedError
    
    def send(self):
        html_content = render_to_string(self.get_template(), self.get_context())
        text_content = self.get_text_content()
        
        email = EmailMultiAlternatives(
            self.get_subject(),
            text_content,
            self.from_email,
            [self.receiver_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    
# Sub classes for each type of email
class ConnectRequestNotification(Notification):
    def get_subject(self):
        subjects = [
            "Look who wants to connect with you! 🤝",
            "New connection request – ready to grow your network? 🌱",
            "Someone’s eager to connect – are you in? 🚀",
            "A fresh connection is waiting for you! Let’s link up! 🔗",
            "Your next connection is just a click away! 📲",
            "Ready to expand your network? New request inside! 🌍",
            "Somebody wants to connect with YOU! 🙌",
            "New connection request alert – let’s make it official! 🔥",
        ]
        return random.choice(subjects)
    
    def get_template(self):
        return "notifications/connect_request_email.html"
    
    def get_context(self):
        return {
            "sender_name": self.sender_name,
            "website_link": "https://oryxalumni.com/profile/"
        }
    
    def get_text_content(self):
        return f"{self.sender_name} wants to connect with you. Visit: https://oryxalumni.com/profile/"

class ConnectAcceptedNotification(Notification):
    def get_subject(self):
        subjects = [
            "You did it! You’re now officially connected! 🎉",
            "Congrats, your connection request has been accepted! 🚀",
            "Welcome to the network – you’re now connected! 🌍",
            "Connection accepted! Let’s make some magic happen! ✨",
            "You’re in! Your connection request has been approved! 🔥",
            "Boom! You’re officially part of the network! 💥",
            "You’ve been accepted! Time to connect and grow! 🌱",
            "It’s official! You’re now connected! 🙌",
            "Connection success! You’re now part of the circle! 🔗",
            "You’ve got a new connection! Let’s do something awesome! 💬",
            "Your connection request was a success! Let’s collaborate! 🤝",
            "You’re now officially connected! Time to shine! 🌟"
        ]
        return random.choice(subjects)
    
    def get_template(self):
        return "notifications/connect_accept_email.html"
    
    def get_context(self):
        return {
            "sender_name": self.sender_name,
            "website_link": "https://oryxalumni.com/messaging/"
        }
    
    def get_text_content(self):
        return f"{self.sender_name} has accepted your connection request. Visit: https://oryxalumni.com/messaging/"
    
class MentorRequestNotification(Notification):
    def get_subject(self):
        subjects = [
            "Look who got a mentor request? 👀",
            "Woah, someone thinks you can guide them! 🙌",
            "Let’s get to work – you’ve got a mentor request!",
            "Your next mentee is waiting! Ready to inspire? 💡",
            "Guess what? Someone wants YOU as their mentor! 🎉",
            "Time to share your wisdom – mentor request incoming!",
            "Your next big mentorship opportunity is here!",
            "You’ve got a new mentee! Let’s make it happen! ✨",
            "Somebody believes you’ve got what it takes to lead! 🔥",
            "Mentorship alert! Are you ready to guide the way? 🌟",
            "Heads up! You’ve got a mentorship request waiting for you! 📨"
        ]
        return random.choice(subjects)
    
    def get_template(self):
        return "notifications/mentor_request_email.html"
    
    def get_context(self):
        return {
            "sender_name": self.sender_name,
            "website_link": "https://oryxalumni.com/mentorship/mentor_dashboard"
        }
    
    def get_text_content(self):
        return f"{self.sender_name} has requested you as their Mentor. Visit: https://oryxalumni.com/mentorship/mentor_dashboard"
    
class MentorAcceptedNotification(Notification):
    def get_subject(self):
        subjects = [
            "You’ve got a mentor! Ready to learn? 🎉",
            "Your mentor just said YES! Let’s get started! 🚀",
            "Boom! Your mentor request has been accepted! 💥",
            "Welcome to mentorship – you’ve got a guide! 🌟",
            "It’s official! You’re now mentored! 🎓",
            "Someone’s ready to guide you – mentorship accepted! 🙌",
            "Your mentorship journey begins now! 🌱",
            "Congrats! You’ve got the mentorship you’ve been waiting for! 🥳",
            "Ready to grow? Your mentor has accepted! 💡",
            "You’ve been matched with a mentor! Time to shine! ✨",
            "Your mentor just accepted! Let’s make things happen! 🔥",
            "You’re in! Your mentor has accepted – let’s get to work! 💪"
        ]
        return random.choice(subjects)
    
    def get_template(self):
        return "notifications/mentor_accept_email.html"
    
    def get_context(self):
        return {
            "sender_name": self.sender_name,
            "website_link": "https://oryxalumni.com/messaging/"
        }
    
    def get_text_content(self):
        return f"{self.sender_name} has accepted your connection request. Visit: https://oryxalumni.com/messaging/"
    
class MentorActivationNotification(Notification):
    def get_subject(self):
        subjects = [
            "Congrats! You’re officially a mentor! 🎉",
            "Welcome to the mentor squad! 🌟",
            "You did it! You’re now a mentor! 🙌",
            "It’s official – you’re a mentor now! Ready to lead? 🚀",
            "You’ve leveled up – welcome to mentorship! 🎓",
            "Time to guide the next generation – you’re a mentor! 💥",
            "Boom! You’re now a mentor! Let’s make an impact! 💡",
            "Your mentorship journey starts now – you’re a mentor! ✨",
            "You’ve got the title! Welcome to mentorship! 🔥",
            "It’s official – you’re a mentor! Let’s get to work! 💪",
            "Your wisdom is in demand – you’re a mentor now! 🌱",
            "Mentor mode: ON! Time to inspire and lead! 🔝"
        ]
        return random.choice(subjects)
    
    def get_template(self):
        return "notifications/mentor_activation_email.html"
    
    def get_context(self):
        return {
            "website_link": "https://oryxalumni.com/mentorship/mentor_dashboard"
        }
    
    def get_text_content(self):
        return "Congrats! You’re officially a mentor! 🎉 Head to your Mentor Dashboard to get started – we’re excited to see you in action! Visit: https://oryxalumni.com/mentorship/mentor_dashboard"

def send_notification(notification):
    threading.Thread(target=notification.send).start()