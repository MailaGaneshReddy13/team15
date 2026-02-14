import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_agent.settings')
django.setup()

from lms.models import Course, Module, Lesson

def create_full_curriculum():
    print("Starting comprehensive LMS content generation...")

    # Python Course (Basics to Advanced)
    python_data = {
        'title': 'Python Mastery: Zero to Hero',
        'description': 'Complete Python Bootcamp: Go from zero to hero in Python 3. Learn Python like a Professional!',
        'category': 'technical',
        'modules': [
            {
                'title': '1. Python Basics',
                'lessons': [
                    {
                        'title': 'Introduction & Setup',
                        'duration': 15,
                        'content': """
                            <h3>What is Python?</h3>
                            <p>Python is a popular programming language. It was created by Guido van Rossum, and released in 1991.</p>
                            <p>It is used for:</p>
                            <ul>
                                <li>Web development (server-side),</li>
                                <li>Software development,</li>
                                <li>Mathematics,</li>
                                <li>System scripting.</li>
                            </ul>
                            <h3>Installation</h3>
                            <p>To verify if Python is installed on your PC, search in the start bar for Python or run the following on the Command Line (cmd.exe):</p>
                            <pre><code>C:\\Users\\Your Name>python --version</code></pre>
                            <p>If not installed, download it for free from the following website: <a href="https://www.python.org/" target="_blank">python.org</a>.</p>
                        """
                    },
                    {
                        'title': 'Variables and Data Types',
                        'duration': 20,
                        'content': """
                            <h3>Variables</h3>
                            <p>Variables are containers for storing data values.</p>
                            <p>Python has no command for declaring a variable. A variable is created the moment you first assign a value to it.</p>
                            <pre><code>x = 5
y = "John"
print(x)
print(y)</code></pre>
                            <h3>Data Types</h3>
                            <p>Built-in Data Types specified by standard:</p>
                            <ul>
                                <li>Text Type: <code>str</code></li>
                                <li>Numeric Types: <code>int</code>, <code>float</code>, <code>complex</code></li>
                                <li>Sequence Types: <code>list</code>, <code>tuple</code>, <code>range</code></li>
                                <li>Mapping Type: <code>dict</code></li>
                                <li>Set Types: <code>set</code>, <code>frozenset</code></li>
                                <li>Boolean Type: <code>bool</code></li>
                            </ul>
                        """
                    }
                ]
            },
            {
                'title': '2. Data Structures',
                'lessons': [
                    {
                        'title': 'Lists & Tuples',
                        'duration': 25,
                        'content': """
                            <h3>Python Lists</h3>
                            <p>Lists are used to store multiple items in a single variable.</p>
                            <p>Lists are one of 4 built-in data types in Python used to store collections of data, the other 3 are Tuple, Set, and Dictionary, all with different qualities and usage.</p>
                            <pre><code>mylist = ["apple", "banana", "cherry"]</code></pre>
                            <h3>List Items</h3>
                            <p>List items are ordered, changeable, and allow duplicate values. List items are indexed, the first item has index [0], the second item has index [1] etc.</p>
                        """
                    },
                    {
                        'title': 'Dictionaries & Sets',
                        'duration': 25,
                        'content': """
                            <h3>Python Dictionaries</h3>
                            <p>Dictionaries are used to store data values in key:value pairs.</p>
                            <p>A dictionary is a collection which is ordered*, changeable and does not allow duplicates.</p>
                            <pre><code>thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}</code></pre>
                        """
                    }
                ]
            },
            {
                'title': '3. Advanced Python',
                'lessons': [
                    {
                        'title': 'Object Oriented Programming (OOP)',
                        'duration': 45,
                        'content': """
                            <h3>Classes and Objects</h3>
                            <p>Python is an object oriented programming language. Almost everything in Python is an object, with its properties and methods.</p>
                            <p>A Class is like an object constructor, or a "blueprint" for creating objects.</p>
                            <pre><code>class MyClass:
  x = 5

p1 = MyClass()
print(p1.x)</code></pre>
                            <h3>The __init__() Function</h3>
                            <p>The examples above are classes and objects in their simplest form, and are not really useful in real life applications.</p>
                            <p>To understand the meaning of classes we have to understand the built-in __init__() function.</p>
                            <p>All classes have a function called __init__(), which is always executed when the class is being initiated.</p>
                        """
                    },
                    {
                        'title': 'Decorators & Generators',
                        'duration': 40,
                        'content': """
                            <h3>Decorators</h3>
                            <p>Decorators are a very powerful and useful tool in Python since it allows programmers to modify the behaviour of a function or class. Decorators allow us to wrap another function in order to extend the behaviour of the wrapped function, without permanently modifying it.</p>
                            <pre><code>def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")</code></pre>
                        """
                    }
                ]
            }
        ]
    }

    # Java Course
    java_data = {
        'title': 'Java Enterprise Development',
        'description': 'Comprehensive Java course covering Core Java, OOPs, Collections, and Multithreading.',
        'category': 'technical',
        'modules': [
            {
                'title': '1. Java Fundamentals',
                'lessons': [
                    {
                        'title': 'JVM Architecture',
                        'duration': 20,
                        'content': """
                            <h3>Java Virtual Machine (JVM)</h3>
                            <p>JVM (Java Virtual Machine) is an abstract machine. It is a specification that provides runtime environment in which java bytecode can be executed.</p>
                            <p>JVMs are available for many hardware and software platforms (i.e. JVM is platform dependent).</p>
                        """
                    },
                    {
                        'title': 'Data Types & Operators',
                        'duration': 20,
                        'content': """
                            <h3>Data Types in Java</h3>
                            <p>Data types specify the different sizes and values that can be stored in the variable. There are two types of data types in Java:</p>
                            <ul>
                                <li><strong>Primitive data types:</strong> The primitive data types include boolean, char, byte, short, int, long, float and double.</li>
                                <li><strong>Non-primitive data types:</strong> The non-primitive data types include Classes, Interfaces, and Arrays.</li>
                            </ul>
                        """
                    }
                ]
            },
            {
                'title': '2. Object Oriented Programming',
                'lessons': [
                    {
                        'title': 'Inheritance & Polymorphism',
                        'duration': 35,
                        'content': """
                            <h3>Inheritance in Java</h3>
                            <p>Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object.</p>
                            <pre><code>class Animal {
  void eat() {
    print("eating...");
  }
}
class Dog extends Animal {
  void bark() {
    print("barking...");
  }
}</code></pre>
                        """
                    }
                ]
            }
        ]
    }

    # React Course
    react_data = {
        'title': 'Modern React.js Development',
        'description': 'Learn React Hooks, Context API, Redux, and build real-world applications.',
        'category': 'technical',
        'modules': [
            {
                'title': '1. React Core',
                'lessons': [
                    {
                        'title': 'JSX & Components',
                        'duration': 20,
                        'content': """
                            <h3>What is JSX?</h3>
                            <p>JSX stands for JavaScript XML. JSX allows us to write HTML in React. JSX makes it easier to write and add HTML in React.</p>
                            <pre><code>const myElement = <h1>I Love JSX!</h1>;</code></pre>
                        """
                    }
                ]
            },
            {
                'title': '2. Hooks',
                'lessons': [
                    {
                        'title': 'useState & useEffect',
                        'duration': 30,
                        'content': """
                            <h3>Hooks</h3>
                            <p>Hooks were added to React in version 16.8.</p>
                            <p>Hooks allow function components to have access to state and other React features. Because of this, class components are generally no longer needed.</p>
                            <pre><code>import { useState } from "react";

function FavoriteColor() {
  const [color, setColor] = useState("red");
  return <h1>My favorite color is {color}!</h1>
}</code></pre>
                        """
                    }
                ]
            }
        ]
    }

    # Soft Skills
    soft_skills_data = {
        'title': 'Professional Communication & Leadership',
        'description': 'Master the soft skills required to accelerate your career growth.',
        'category': 'soft_skills',
        'modules': [
            {
                'title': '1. Effective Communication',
                'lessons': [
                    {
                        'title': 'Active Listening',
                        'duration': 15,
                        'content': """
                            <h3>The Art of Active Listening</h3>
                            <p>Active listening is a pattern of listening that keeps you engaged with your conversation partner in a positive way. It is the process of listening attentively while someone else speaks, paraphrasing and reflecting back what is said, and withholding judgment and advice.</p>
                        """
                    }
                ]
            },
            {
                'title': '2. Leadership',
                'lessons': [
                    {
                        'title': 'Conflict Resolution',
                        'duration': 25,
                        'content': """
                            <h3>Managing Conflict</h3>
                            <p>Conflict in the workplace is inevitable. The ability to resolve conflict effectively is a crucial skill for everyone, from an entry-level employee to a CEO.</p>
                        """
                    }
                ]
            }
        ]
    }

    # List of all courses to create
    all_courses = [python_data, java_data, react_data, soft_skills_data]

    for course_data in all_courses:
        # Create Course
        course, _ = Course.objects.get_or_create(
            title=course_data['title'],
            defaults={
                'description': course_data['description'],
                'category': course_data['category']
            }
        )
        # Update description if exists
        course.description = course_data['description']
        course.save()

        print(f"Processing Course: {course.title}")

        for i, module_data in enumerate(course_data['modules']):
            # Create Module
            module, _ = Module.objects.update_or_create(
                course=course,
                title=module_data['title'],
                defaults={'order': i + 1}
            )
            
            for j, lesson_data in enumerate(module_data['lessons']):
                # Create Lesson
                Lesson.objects.update_or_create(
                    module=module,
                    title=lesson_data['title'],
                    defaults={
                        'content': lesson_data['content'],
                        'duration_minutes': lesson_data['duration'],
                        'order': j + 1
                    }
                )

    print("All curriculum data generated successfully!")

if __name__ == '__main__':
    create_full_curriculum()
