# Traveling Salesperson Problem Application

Base setup for use case apps. 

## Description
This app provides the base setup for a use case application. It is a FastAPI web app, that provides documentation for a given use case, a nice UI for configuring a use case instance and a solution visualization of a solved use case instance. After a submitted configuration this app is going to create and return a workload e.g. QUBO. 

This app will not save any use case instances or solutions in a database. Its only task is to visually guide the user (i.e., domain expert) through the use case documentation and configuration process, as well as returning a workload to the QuCUN Platform, in which this use case application is integrated via an [iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe?). 

### Customization
This template application needs to be customized according to your target use case. URLs and template texts need to be adjusted. The logic for creating the workload (i.e. QUBO) needs to be added. The html files in the templates folder only contain code that you will likely need anyways, but without any actual user input interface, use case specific documentation or texts as well as correct sendinh and handling of HTTP requests. 

A lot but not all of those tasks are marked with a "TODO" in comment form.

## Running the App
For now we're running the project simply with a virtual environment.
Create the environment e.g. on Ubuntu with:

    python3 -m venv venv

Activate the environment and then install packages with: 

    pip install -r requirements.txt

Then using uvicorn you can run the app on localhost with e.g. 

    uvicorn app.main:app --reload   

Feel free to run the project however you want. Docker or poetry are also an option!

## Project Structure 
The project is a web app based on FastAPI and follows its basic structure. Most files of this project provide a lot of comments and helpful information. For a deeper understanding check out the [FastAPI documentation](https://fastapi.tiangolo.com/).

## Userflow
The user navigates between description, configuration and solution visualization through the QuCUN platform, which will send requests via postmessages. The landing page of the use case is its description and from there the configuration UI as well as the solution visualization are loaded in a modal, that shows as an overlay, when the platform requests a page change. So the modals are already available in the description template, but only visible (toggled between being visible or hidden), when the user requests it. The content, like solution visualization, will be generated, when the modal is requested.

## Templates
We use Jinja as a templating engine. It provides a lot of usefull functionalities like for loops and if else clauses. See the [Jinja documentation](https://jinja.palletsprojects.com/en/3.1.x/) for a detailed explaination.

### Template Inheritance
Via inheritance ([see Jinja documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance)) [base.html](./app/templates/base.html) is used as a parent template that loads style and script files used in all or multiple templates. If a navigation bar or footer is needed, it wil lalso be added here, so it is coherent across all templates. 

Child templates extend base.html and add the html code as well as style and script, that are only used in the child. 

## Styling
Apart from custom CSS we will use [TailwindCSS](https://tailwindcss.com/docs) for styling the use cases. This is temporary, until we have a specific styling provided by QuCUN (i.e., the design agency hired by QuCUN).
TailwindCSS is not to be confused with TailwindUI or Components.

This thirdparty [Tailwind cheatsheet](https://nerdcave.com/tailwind-cheat-sheet) provides an overview over all tailwind classes with documentation and examples.
When looking for specific attributes like font-sizes or margins, you simply search for it and add the class that fits your needs into the style attribute of the html element that you want to style.

When using VSCode I recommend the Tailwind CSS IntelliSense extension. 

### Styled Components
[Flowbite](https://flowbite.com/docs/getting-started/introduction/) is an open-source library that provides 600+ styled UI components like buttons and form elements, all using TailwindCSS. They can easily be integrated into this project by just copying and pasting the provided code. 
These components are pretty, responsive and often dark and light mode reactive. So whenever you need something simple, I would suggest to look here. 
These components can also very easily be further customized. 

### Icons
Flowbite provides icons, which it also uses in its components here: [Flowbite Icons](https://flowbite.com/icons/).
Another open source icon library, which is linked in the Tailwind documentation is [Heroicons](https://heroicons.dev/).
For the sake of consistency I would suggest to stick to Flowbite icons and make use of Heroicons or other open-source SVG icons when Flowbite does not provide what you need. 

## Scripting
As a scripting language we will use [Hyperscript](https://hyperscript.org/docs/).
When Hyperscript reaches its limits we can use Javascript, either within Hyperscript in the form of a js .. end block or in its own script block in the template. 

If needed we can use Javascript libraries that provide functionalities that we want, but are too complex or not worth implementing ourselves. Integrating JQuery into the project might be necessary for this. If you're unsure about using external Javascript libraries, just consult with your team. It is a decision often based on a trade-off of losing customizability and implementation time. 

## Communication between QuCUN Platform and Use Case
The QuCUN platform nests every use case in an iframe. They will communicate through the [postMessage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage). 

### Security
When sending messages through postMessage it is important to set the targetOrigin to stop the messages from being send to malicios websites (e.g. if the iframe is compromised and links to a website other then our use case). Never use the wildcard ``` "*" ``` as the targetOrigin, as it is set in this template repository. 



When receiving messages through an eventListener it is important to verify the sender’s identity using the origin.

    window.addEventListener("message", (event) => {
        if (event.origin !== "http://example.org:8080")
        return;
        // ...
    }, false);

