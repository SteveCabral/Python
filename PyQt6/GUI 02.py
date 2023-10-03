from PyQt6.QtWidgets import QApplication, QWidget

# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Create an instance of QApplication, passing in sys.arg, 
# which is Python list containing the command line arguments passed to the application.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)


# Create a Qt widget, which will be our window.
# In Qt all top level widgets are windows -- that is, they don't have a parent and are not nested within another widget or layout. 
# This means you can technically create a window using any widget you like.
window = QWidget()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.


# Start the event loop.
# What's the event loop?
# Before getting the window on the screen, there are a few key concepts to introduce about how applications are organized in the Qt world. If you're already familiar with event loops you can safely skip to the next section.
# The core of every Qt Applications is the QApplication class. 
# Every application needs one — and only one — QApplication object to function. 
# This object holds the event loop of your application — the core loop which governs all user interaction with the GUI.
app.exec()

# Each interaction with your application — whether a press of a key, click of a mouse, or mouse movement — 
# generates an event which is placed on the event queue. 
# In the event loop, the queue is checked on each iteration and if a waiting event is found, 
# the event and control is passed to the specific event handler for the event. 
# The event handler deals with the event, then passes control back to the event loop to wait for more events. 
# There is only one running event loop per application.

# The QApplication class - QApplication holds the Qt event loop - One QApplication instance required - 
# Your application sits waiting in the event loop until an action is taken - 
# There is only one event loop running at any time

# Your application won't reach here until you exit and the event
# loop has stopped.