from database.models import *


def seed_db():
    # Obviously not secure, for demonstration only
    admin = User(username="admin", display_name="Addison Min", password_hash=hex(hash("banana")),
                 photo_filename="admin.jpg", is_admin=True)
    bobby = User(username="bobby", display_name="Bobby Tables", password_hash=hex(hash("hunter2")),
                 photo_filename="bob.jpg", is_admin=False)
    alice = User(username="alice", display_name="Alice in Wonderland", password_hash=hex(hash("passw0rd")),
                 photo_filename="alice.jpg", is_admin=False)
    for user in (admin, bobby, alice):
        user.save()

    # Insert posts
    Post(author=bobby, post_text="Just had a great coffee! ☕ Thinking about starting a new project. Any ideas? #coffee "
                                 "#projectideas #newbeginnings").save()
    Post(author=alice, post_text="Learning so much in my coding bootcamp! Today we covered CSS Grid and it's blowing "
                                 "my mind 🤯. #coding #cssgrid #webdev #bootcamp").save()
    Post(author=admin, post_text="Breaking News: New smartphone announced with incredible camera features and a "
                                 "revolutionary processor! More details to come. #tech #smartphone #newtech").save()
    Post(author=alice, post_text="Check out this amazing sunset from my walk earlier! 🌅 Nature is so beautiful. "
                                 "#sunset #nature #photography #beautiful").save()
    Post(author=bobby, post_text="What are your favorite cybersecurity innovations from the last five years? #cyber "
                                 "#innovation #technology").save()
