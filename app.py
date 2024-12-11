import streamlit as st
import os
import shutil

# загрузки схем
def load_schemes():
    if os.path.exists("schemes.barfi"):
        with open("schemes.barfi", "r") as f:
            return f.read()
    return ""

# сохранения схем
def save_schemes(content):
    with open("schemes.barfi", "w") as f:
        f.write(content)

# дублирования схем
def duplicate_scheme(scheme_name):
    if os.path.exists(scheme_name):
        shutil.copy(scheme_name, f"copy_{scheme_name}")

# удаления схем
def delete_scheme(scheme_name):
    if os.path.exists(scheme_name):
        os.remove(scheme_name)

# Интерфейс Streamlit
st.title("Управление потоком Barfi")

# загрузка схем
schemes_content = load_schemes()

st.text_area("Текущие схемы", schemes_content, height=300)

# добавление функционала для сохранения, удаления и дублирования схем
with st.expander("Управление схемами"):
    new_scheme = st.text_input("Введите новую схему")
    if st.button("Схема сохранения"):
        save_schemes(new_scheme)
        st.success("Scheme saved successfully!")

    if st.button("Дублирующая схема"):
        scheme_to_duplicate = st.text_input("Enter the name of the scheme to duplicate")
        duplicate_scheme(scheme_to_duplicate)
        st.success(f"Scheme {scheme_to_duplicate} duplicated.")

    if st.button("Удалить схему"):
        scheme_to_delete = st.text_input("Enter the name of the scheme to delete")
        delete_scheme(scheme_to_delete)
        st.success(f"Scheme {scheme_to_delete} deleted.")
