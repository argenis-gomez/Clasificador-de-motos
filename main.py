import streamlit as st
import SessionState
from utils import load_model, return_prediction
import os
import time


def rerun(session_state):
    session_state.pred_button = False
    session_state.feedback = "Seleccione una opción"
    session_state.feedback_2 = "Seleccione una opción"

    st.write(f"Reiniciando app...")
    time.sleep(1)
    st.experimental_rerun()

    return session_state


def feedback(session_state, value, classes=None):
    session_state.feedback = st.selectbox("¿Es correcta la predicción?",
                            ("Seleccione una opción", "Si", "No"))

    if session_state.feedback == "Seleccione una opción":
        pass
    elif session_state.feedback == "Si":
        st.write("Si desea puede ayudarnos clasificando otras imágenes de motos.")
        if value:
            with open(f'datasets/data1/no_motos/no_moto_{len(os.listdir("datasets/data1/no_motos")):04d}.jpg',
                      'wb') as f:
                f.write(session_state.uploaded_image)
                print('Imagen guardada en datasets/data1/no_motos...')
        else:
            with open(f'datasets/data1/motos/moto_{len(os.listdir("datasets/data1/motos")):04d}.jpg',
                      'wb') as f:
                f.write(session_state.uploaded_image)
                print('Imagen guardada en datasets/data1/motos...')
            if classes == 0:
                with open(f'datasets/data3/clasicas/clasica_{len(os.listdir("datasets/data3/clasicas")):04d}.jpg',
                          'wb') as f:
                    f.write(session_state.uploaded_image)
                    print('Imagen guardada en datasets/data3/clasicas...')
            elif classes == 1:
                with open(f'datasets/data3/deportivas/deportiva_{len(os.listdir("datasets/data3/deportivas")):04d}.jpg',
                          'wb') as f:
                    f.write(session_state.uploaded_image)
                    print('Imagen guardada en datasets/data3/deportivas/deportiva_...')
            else:
                with open(f'datasets/data3/scooter/scooter_{len(os.listdir("datasets/data3/scooter")):04d}.jpg',
                          'wb') as f:
                    f.write(session_state.uploaded_image)
                    print('Imagen guardada en datasets/data3/scooter...')

        session_state = rerun(session_state)

    else:
        st.write("Seguiremos trabajando en mejorar nuestras predicciones.")
        if value:

            with open(f'datasets/data1/motos/moto_{len(os.listdir("datasets/data1/motos")):04d}.jpg',
                      'wb') as f:
                f.write(session_state.uploaded_image)
                print('Imagen guardada en datasets/data1/motos...')

            session_state.feedback_2 = st.selectbox("¿Que clase de moto es:?",
                                                  ("Seleccione una opción", "Clásica", "Deportiva", "Scooter"))

            if session_state.feedback_2 == "Seleccione una opción":
                pass

            if session_state.feedback_2 == "Clásica":
                with open(f'datasets/data3/clasicas/clasica_{len(os.listdir("datasets/data3/clasicas")):04d}.jpg',
                          'wb') as f:
                    f.write(session_state.uploaded_image)
                    print('Imagen guardada en datasets/data3/clasicas...')
            elif session_state.feedback_2 == "Deportiva":
                with open(f'datasets/data3/deportivas/deportiva_{len(os.listdir("datasets/data3/deportivas")):04d}.jpg',
                          'wb') as f:
                    f.write(session_state.uploaded_image)
                    print('Imagen guardada en datasets/data3/deportivas/deportiva_...')
            else:
                with open(f'datasets/data3/scooter/scooter_{len(os.listdir("datasets/data3/scooter")):04d}.jpg',
                          'wb') as f:
                    f.write(session_state.uploaded_image)
                    print('Imagen guardada en datasets/data3/scooter...')
        else:
            with open(f'datasets/data1/no_motos/no_moto_{len(os.listdir("datasets/data1/no_motos"))+1:03d}.jpg',
                      'wb') as f:
                f.write(session_state.uploaded_image)
                print('Imagen guardada en datasets/data1/no_motos...')

        session_state = rerun(session_state)

    return session_state


def main():

    st.title('Clasificador de motos')

    st.header("A continuación un clasificador de motos:")

    uploaded_file = st.file_uploader(label="Selecciona una imagen de moto:",
                                     type=["png", "jpeg", "jpg"])

    session_state = SessionState.get(pred_button=False)

    if not uploaded_file:
        st.warning("Por favor subir una imagen.")
        st.stop()
    else:
        session_state.uploaded_image = uploaded_file.read()
        st.image(session_state.uploaded_image, width=250)

        if st.button('Identificar'):
            session_state.pred_button = True

        if session_state.pred_button:

            label, value = return_prediction(session_state.uploaded_image, MODEL_1, IMG_SHAPE, False)

            if value:
                st.write(f"Su predicción {label}.")
                session_state = feedback(session_state, value)
            else:
                label, classes = return_prediction(session_state.uploaded_image, MODEL_2, IMG_SHAPE, True)
                st.write(f"Su predicción es una moto {label}.")
                session_state = feedback(session_state, value, classes)


if __name__ == '__main__':
    IMG_SHAPE = (299, 299)
    MODEL_1 = load_model('modelos/modelo1/modelo_1.h5')
    MODEL_2 = load_model('modelos/modelo2/modelo_2.h5')

    main()
