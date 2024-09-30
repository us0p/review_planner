# Review Planner
A CLI application to help you schedule your revisions to increase information retention.  
The project is based on the [spaced repetition](https://e-student.org/spaced-repetition/)
technique.  
The goal of the project is to provide a simple and efficient tool to help space your
revisions and track what need to be done and when.  
For bether studying sessions it's indicated to also apply the 
[active recall](https://e-student.org/active-recall-study-method/) study method during the 
revisions.

# Dependencies and Requirements
The project is intended to run under Unix systems, it doesn't have Windows support.

System dependencies:
- python >= 3.11
- pip >= 23.0.1

# Build and Install
To build and install the project:
- make build.sh executable and run.

```bash
chmod +x build.sh && ./build.sh
```

- after reloading bash configuration or opening a new terminal, esure the program is installed 
with:
```bash
reviewpln -h
```

The project uses the package [Pyinstaller](https://pyinstaller.org/en/stable/index.html) to
bundle the modules and packages of the project as a single executable.
>The build script assumes you have ~/local/share/bin in your $PATH.
