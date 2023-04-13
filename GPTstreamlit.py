import streamlit as st
import random
import pandas as pd
import numpy as np
import subprocess
import shutil
import os



tags=[]

problem_files = {
        "Números complexos": [file for file in os.listdir("./MA044") if file.startswith("Números complexos")],
        "Funções de variável complexa": [file for file in os.listdir("./MA044") if file.startswith("Funções de variável complexa")],
        "Equações de Cauchy-Riemann": [file for file in os.listdir("./MA044") if file.startswith("Equações de Cauchy-Riemann")]
    }





def append_and_convert_to_tex(TeXt):
    shutil.copy2("cabeçalho.txt", "cabeçalho_copy.txt")

    
    with open("cabeçalho_copy.txt", "a") as file:
        #text_to_append = st.text_input(TeXt)
        file.write(TeXt)
    
    with open("cabeçalho_copy.txt", "r") as file:
        text = file.read()
        
    with open("cabeçalho_copy.tex", "w") as file:
        file.write(text)
        #st.download_button("teste.tex", "cabeçalho_copy.tex", "Download test")

    subprocess.run(["pdflatex", "cabeçalho_copy.tex"])
    
    with open("cabeçalho_copy.pdf", "rb") as file:
         pdf = file.read()
         st.download_button("Baixar Simulado-MA044", file , "Simulado-MA044")
  




    


def create_check_boxes():
    st.sidebar.write('Ementa:')
    keys = problem_files.keys()
    check_boxes = [st.sidebar.checkbox(j, key=j) for j in keys]
    col1 = [j for j, checked in zip(keys, check_boxes) if checked]
    return col1







def create_random_test(file_contents, TAGS):
    # Extract the questions from the .tex file and store them in a list
    questions = []
    current_question = ""
    for line in file_contents.split("\n"):
      #for t in TAGS: 
        if "\problem" in line:
            if current_question:
                questions.append(current_question)
            current_question = ""
        else:
            current_question += line + "\n"
    if current_question:
        questions.append(current_question)
    
    # Select a random set of questions
    num_questions = min(5, len(questions))
    selected_questions = random.sample(questions, num_questions)
    
    # Create the test as a .tex file
    test_contents = "\n\n \\begin{enumerate}\n"
    for question in selected_questions:
        test_contents += "\\item " + question + "\n"
    test_contents += "\\end{enumerate}\n\n \\end{document}"
    
    return test_contents








def main():
    st.markdown("<style>body { background-color: powderblue; }</style>", unsafe_allow_html=True)
    st.title("Gerador de Simulados")
    TAGS=[]
    #st.set_page_config(page_title="Gerador de Simulados", page_icon=":book:", layout="wide")
    
    
    uploaded_file = st.file_uploader("Upload a .tex file with problems:", type=["tex"])
    if uploaded_file is not None:
        file_contents = uploaded_file.read().decode()
        tags=create_check_boxes()
        #st.write("The selected tags are:")
        #print(tags)
        TAGS=tags
        test_contents = create_random_test(file_contents, TAGS)
        test_contents_app=append_and_convert_to_tex(test_contents)
        #st.write("Generated test:")
        #st.latex(test_contents_app)
        #st.markdown("Download the test:")
        #st.download_button("test.tex", test_contents_app, "Download test")


        

if __name__ == "__main__":
    main()
